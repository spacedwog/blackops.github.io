import java.awt.*;
import java.net.URL;
import javax.swing.*;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.awt.event.ActionEvent;
import java.net.HttpURLConnection;
import java.awt.event.ActionListener;

public class BlackOpsAPIClient extends JFrame {

    private JButton checkButton;
    private JEditorPane htmlPane;
    private JButton relayOnButton;
    private JButton relayOffButton;
    private JTextArea responseArea;
    private JProgressBar progressBar;
    private MatrixBackgroundPanel matrixBackgroundPanel;

    public BlackOpsAPIClient() {
        setTitle("🖥️ BlackOps API Client");
        setSize(600, 400);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());
        
        // Adiciona o painel de fundo animado estilo Matrix
        matrixBackgroundPanel = new MatrixBackgroundPanel();
        matrixBackgroundPanel.setPreferredSize(new Dimension(600, 400));
        add(matrixBackgroundPanel, BorderLayout.CENTER);
        
        // Criar componentes
        Font font = new Font("Arial", Font.PLAIN, 14);
        
        responseArea = new JTextArea();
        responseArea.setEditable(false);
        responseArea.setFont(font);
        responseArea.setLineWrap(true);
        responseArea.setWrapStyleWord(true);
        JScrollPane scrollPane = new JScrollPane(responseArea);
        scrollPane.setBorder(BorderFactory.createLineBorder(Color.GRAY));

        checkButton = new JButton("🔍 Consultar Status da API");
        checkButton.setFont(font);
        checkButton.setBackground(new Color(52, 152, 219));
        checkButton.setForeground(Color.WHITE);
        checkButton.setFocusPainted(false);
        checkButton.setBorder(BorderFactory.createLineBorder(new Color(41, 128, 185)));

        relayOnButton = new JButton("⚡ Ligar Relay");
        relayOnButton.setFont(font);
        relayOnButton.setBackground(new Color(39, 174, 96)); // Verde
        relayOnButton.setForeground(Color.WHITE);
        relayOnButton.setFocusPainted(false);

        relayOffButton = new JButton("⛔ Desligar Relay");
        relayOffButton.setFont(font);
        relayOffButton.setBackground(new Color(192, 57, 43)); // Vermelho
        relayOffButton.setForeground(Color.WHITE);
        relayOffButton.setFocusPainted(false);

        progressBar = new JProgressBar();
        progressBar.setIndeterminate(true);
        progressBar.setString("Conectando...");
        progressBar.setStringPainted(true);
        progressBar.setVisible(false);

        // Ação do botão
        checkButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                checkStatus();
            }
        });
        
        relayOnButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                sendRelayCommand("on");
            }
        });
        
        relayOffButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                sendRelayCommand("off");
            }
        });

        // Layout
        JPanel panel = new JPanel();
        panel.setLayout(new FlowLayout(FlowLayout.CENTER, 10, 20));
        panel.setBackground(new Color(249, 250, 252));

        panel.add(checkButton);
        panel.add(progressBar);
        panel.add(relayOnButton);
        panel.add(relayOffButton);
        
        add(panel, BorderLayout.NORTH);
        add(scrollPane, BorderLayout.CENTER);

        // JEditorPane para HTML
        htmlPane = new JEditorPane();
        htmlPane.setEditable(false);
        htmlPane.setContentType("text/html"); // Define o tipo de conteúdo como HTML
        JScrollPane htmlScroll = new JScrollPane(htmlPane);
        
        // Layout de exibição
        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, scrollPane, htmlScroll);
        splitPane.setDividerLocation(300);  // Ajuste a posição do painel
        add(splitPane, BorderLayout.CENTER);

        setLocationRelativeTo(null); // Centralizar janela
        setVisible(true);
    }

    public void checkStatus() {
        // Exibir o progresso enquanto faz a conexão
        progressBar.setVisible(true);
        responseArea.setText("🔄 Conectando... Aguarde.");
    
        try {
            // Simular conexão com a API
            URL url = new URL("http://localhost:8502");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
    
            int responseCode = conn.getResponseCode();
            responseArea.setText("🔗 Conexão feita! Código de resposta: " + responseCode + "\n");
    
            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder response = new StringBuilder();
                String line;
    
                while ((line = reader.readLine()) != null) {
                    response.append(line).append("\n");
                }
                reader.close();
    
                // Verifique se a resposta é HTML
                if (response.toString().contains("<!DOCTYPE html>")) {
                    // Exibir HTML diretamente no JEditorPane
                    htmlPane.setText(response.toString());
                }
                else {
                    // Caso contrário, tratar como JSON
                    try {
                        JSONObject jsonResponse = new JSONObject(response.toString());
                        String status = jsonResponse.getString("status");
                        String message = jsonResponse.getString("message");
                
                        responseArea.append("✅ Status: " + status + "\n");
                        responseArea.append("📝 Mensagem: " + message + "\n");
                    } catch (Exception ex) {
                        responseArea.append("⚠️ Erro ao processar resposta JSON: " + ex.getMessage());
                    }
                }                
            } else {
                responseArea.append("⚠️ Falha na conexão. Código: " + responseCode);
            }
        } catch (Exception e) {
            responseArea.setText("❌ Erro ao conectar com a API:\n" + e.getMessage());
            e.printStackTrace();
        } finally {
            // Após a resposta, ocultar a barra de progresso
            progressBar.setVisible(false);
        }
    }
    
    private void sendRelayCommand(String command) {
        progressBar.setVisible(true);
        responseArea.setText("🔄 Enviando comando: " + command + "...");
    
        try {
            URL url = new URL("http://localhost:8502/relay/" + command);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST"); // Ou "GET" dependendo da sua API!
    
            int responseCode = conn.getResponseCode();
            responseArea.setText("📡 Comando enviado! Código de resposta: " + responseCode + "\n");
    
            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder response = new StringBuilder();
                String line;
    
                while ((line = reader.readLine()) != null) {
                    response.append(line).append("\n");
                }
                reader.close();
    
                responseArea.append("✅ Resposta:\n" + response.toString());
            } else {
                responseArea.append("⚠️ Falha ao enviar comando. Código: " + responseCode);
            }
        } catch (Exception e) {
            responseArea.setText("❌ Erro ao enviar comando:\n" + e.getMessage());
            e.printStackTrace();
        } finally {
            progressBar.setVisible(false);
        }
    }    

    public static void main(String[] args) {
        // Executar na Thread correta (boa prática em aplicações Swing)
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new BlackOpsAPIClient();
            }
        });
    }

    // Painel customizado para o background estilo Matrix
    private class MatrixBackgroundPanel extends JPanel {
        private final int COLS = 60; // Número de colunas
        private final int FONT_SIZE = 20; // Tamanho da fonte

        private final char[] chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".toCharArray(); // Caracteres aleatórios
        private int[] drops = new int[COLS]; // Posições dos caracteres caindo

        public MatrixBackgroundPanel() {
            setBackground(Color.BLACK);
            setOpaque(false); // Deixar o painel transparente para ver a animação

            // Iniciar um thread para a animação
            Thread matrixThread = new Thread(new Runnable() {
                @Override
                public void run() {
                    while (true) {
                        repaint(); // Atualiza o painel a cada iteração
                        try {
                            Thread.sleep(50); // Atualizar a cada 50 ms
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                }
            });
            matrixThread.start();
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2d = (Graphics2D) g;
            g2d.setColor(new Color(0, 255, 0, 150)); // Cor verde brilhante com transparência
            g2d.setFont(new Font("Monospaced", Font.PLAIN, FONT_SIZE));

            for (int i = 0; i < COLS; i++) {
                // Aleatoriamente desenha caracteres
                g2d.drawString(String.valueOf(chars[(int) (Math.random() * chars.length)]), i * FONT_SIZE, drops[i] * FONT_SIZE);

                // Reseta a posição quando ela chega no fundo
                if (drops[i] * FONT_SIZE > getHeight() && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }
    }
}