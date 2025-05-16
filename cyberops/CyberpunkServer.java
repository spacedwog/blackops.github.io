
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

public class CyberpunkServer {

    public static void main(String[] args) {
        int port = 8080;

        try (ServerSocket serverSocket = new ServerSocket(port, 50, InetAddress.getByName("192.168.15.138"))) {
            System.out.println("Cyberpunk Java Server is running on port " + port + "...");

            while (true) {
                try (
                        Socket clientSocket = serverSocket.accept(); BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream())); PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true)) {
                    String requestLine = in.readLine();
                    System.out.println("Received: " + requestLine);

                    if (requestLine != null) {
                        String[] parts = requestLine.split(" ");
                        if (parts.length >= 2) {
                            String method = parts[0];
                            String path = parts[1];
                            String body;

                            if ("GET".equals(method)) {
                                switch (path) {
                                    case "/STATUS" -> {
                                        body = "[JAVA]STATE:ON";
                                        sendResponse(out, 200, "text/plain", body);
                                    }

                                    case "/BLOCKED" -> {
                                        body = "[JAVA]BLOCKED_REASONS:\n- IP Suspeito\n- DNS inválido\n- Firewall ativo";
                                        sendResponse(out, 200, "text/plain", body);
                                    }

                                    case "/DIAGNOSE" -> {
                                        body = "[JAVA]DIAGNOSIS:\n- Verifique a conexão com o GitHub\n- Certifique-se de que os pacotes estão autorizados";
                                        sendResponse(out, 200, "text/plain", body);
                                    }

                                    case "/CYBERBRAIN" -> {
                                        body = "[JAVA]{\"ai\":\"active\",\"level\":\"autonomous\",\"protection\":\"enabled\"}";
                                        sendResponse(out, 200, "application/json", body);
                                    }

                                    case "/EXPORT" -> {
                                        body = "[JAVA]{\"status\":\"success\",\"path\":\"/dados_github/dados_usuario.json\"}";
                                        sendResponse(out, 200, "application/json", body);
                                    }

                                    default ->
                                        sendResponse(out, 404, "text/plain", "404 Not Found");
                                }
                            } else {
                                sendResponse(out, 405, "text/plain", "405 Method Not Allowed");
                            }
                        }
                    }

                } catch (IOException e) {
                    System.err.println("Erro ao processar cliente: " + e.getMessage());
                }
            }

        } catch (IOException e) {
            System.err.println("Erro ao iniciar o servidor: " + e);
        }
    }

    private static void sendResponse(PrintWriter out, int statusCode, String contentType, String body) {
        String statusText = switch (statusCode) {
            case 200 ->
                "OK";
            case 404 ->
                "Not Found";
            case 405 ->
                "Method Not Allowed";
            default ->
                "Error";
        };

        out.print("[JAVA]HTTP/1.1 " + statusCode + " " + statusText + "\r\n");
        out.print("Content-Type: " + contentType + "\r\n");
        out.print("Content-Length: " + body.length() + "\r\n");
        out.print("Connection: close\r\n");
        out.print("\r\n");
        out.print(body);
        out.flush();
    }
}
