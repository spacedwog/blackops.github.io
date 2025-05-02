import java.sql.Connection;
import java.sql.SQLException;
import java.sql.DriverManager;

public class SQLiteConnection {
    public static void main(String[] args) {
        String url = "jdbc:sqlite:clusterops.db"; // Caminho do arquivo .db

        try (Connection conn = DriverManager.getConnection(url)) {
            if (conn != null) {
                System.out.println("Conexão com SQLite estabelecida.");
            }
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }
}