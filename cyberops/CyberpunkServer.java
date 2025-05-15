import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

public class CyberpunkServer {
    public static void main(String[] args) {
        int port = 8080; // Porta a escutar
        try (ServerSocket serverSocket = new ServerSocket(port, 50, InetAddress.getByName("192.168.15.8"));) {
            System.out.println("Cyberpunk Java Server is running on port " + port + "...");

            while (true) {
                try (Socket clientSocket = serverSocket.accept()) {
                    BufferedReader in = new BufferedReader(
                            new InputStreamReader(clientSocket.getInputStream()));
                    PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
                    
                    String inputLine = in.readLine();
                    System.out.println("Received: " + inputLine);
                    
                    // Lógica de resposta (você pode integrar com métodos Java reais aqui)
                    String response = "[JAVA] Resposta: " + inputLine;
                    out.println(response);
                }
            }
        } catch (IOException e) {
            System.out.println("Ocorreu um erro" + e.toString());
        }
    }
}