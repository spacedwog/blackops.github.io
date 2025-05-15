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

        try (ServerSocket serverSocket = new ServerSocket(port, 50, InetAddress.getByName("192.168.15.8"))) {
            System.out.println("Cyberpunk Java Server is running on port " + port + "...");

            while (true) {
                try (Socket clientSocket = serverSocket.accept();
                     BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                     PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true)) {

                    String requestLine = in.readLine();
                    System.out.println("Received: " + requestLine);

                    if (requestLine != null) {
                        String[] parts = requestLine.split(" ");
                        if (parts.length >= 2) {
                            String method = parts[0];
                            String path = parts[1];

                            if ("GET".equals(method) && "/STATUS".equals(path)) {
                                String body = "STATE:ON";

                                out.print("[JAVA]HTTP/1.1 200 OK\r\n");
                                out.print("Content-Type: text/plain\r\n");
                                out.print("Content-Length: " + body.length() + "\r\n");
                                out.print("Connection: close\r\n");
                                out.print("\r\n");
                                out.print(body);
                            } else {
                                String body = "404 Not Found";
                                out.print("HTTP/1.1 404 Not Found\r\n");
                                out.print("Content-Type: text/plain\r\n");
                                out.print("Content-Length: " + body.length() + "\r\n");
                                out.print("Connection: close\r\n");
                                out.print("\r\n");
                                out.print(body);
                            }
                            out.flush();
                        }
                    }

                } catch (IOException e) {
                    System.out.println("Erro ao processar cliente: " + e.getMessage());
                }
            }

        } catch (IOException e) {
            System.out.println("Erro ao iniciar o servidor: " + e);
        }
    }
}