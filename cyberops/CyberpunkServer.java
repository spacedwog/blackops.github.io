import java.io.*;
import java.net.*;

public class CyberpunkServer {
    public static void main(String[] args) {
        int port = 9999; // Porta a escutar
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Cyberpunk Java Server is running on port " + port + "...");

            while (true) {
                Socket clientSocket = serverSocket.accept();
                BufferedReader in = new BufferedReader(
                    new InputStreamReader(clientSocket.getInputStream()));
                PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);

                String inputLine = in.readLine();
                System.out.println("Received: " + inputLine);

                // Lógica de resposta (você pode integrar com métodos Java reais aqui)
                String response = "[JAVA] Ack: " + inputLine;
                out.println(response);

                clientSocket.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}