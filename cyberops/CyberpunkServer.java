import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

public class CyberpunkServer {
    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress("192.168.15.8", 8080), 0);
        server.createContext("/", new MyHandler());
        server.setExecutor(null); // Usa executor padrão
        System.out.println("Servidor HTTP Java rodando em http://192.168.15.8:8080/");
        server.start();
    }

    static class MyHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String resposta = "{\"message\": \"Olá do servidor Java via HTTP!\"}";
            exchange.getResponseHeaders().add("Content-Type", "application/json");
            exchange.sendResponseHeaders(200, resposta.length());
            OutputStream os = exchange.getResponseBody();
            os.write(resposta.getBytes());
            os.close();
        }
    }
}