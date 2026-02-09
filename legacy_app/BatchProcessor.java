package legacy_app;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Date;

/**
 * BatchProcessor.java
 * Simulates a legacy nightly batch job that processes transactions.
 * In a real scenario, this would be a complex enterprise job.
 */
public class BatchProcessor {

    private static final String DB_URL = "jdbc:sqlite:../database/legacy_system.db";

    public static void main(String[] args) {
        System.out.println("Starting Nightly Batch Process at " + new Date());
        
        try (Connection conn = DriverManager.getConnection(DB_URL)) {
            // Simulate processing pending transactions
            processTransactions(conn);
            
            // Simulate generating a nightly report summary
            generateNightlyReport(conn);
            
        } catch (SQLException e) {
            System.err.println("Database connection failed: " + e.getMessage());
            e.printStackTrace();
        }
        
        System.out.println("Batch Process Completed at " + new Date());
    }

    private static void processTransactions(Connection conn) throws SQLException {
        System.out.println("Scanning for pending transactions...");
        String query = "SELECT count(*) FROM transactions WHERE status = 'PENDING'";
        try (PreparedStatement pstmt = conn.prepareStatement(query);
             ResultSet rs = pstmt.executeQuery()) {
            if (rs.next()) {
                int pendingCount = rs.getInt(1);
                System.out.println("Found " + pendingCount + " pending transactions. Processing...");
                
                // Simulate update
                String update = "UPDATE transactions SET status = 'PROCESSED', processed_at = CURRENT_TIMESTAMP WHERE status = 'PENDING'";
                try (PreparedStatement updateStmt = conn.prepareStatement(update)) {
                    int rows = updateStmt.executeUpdate();
                    System.out.println("Successfully processed " + rows + " transactions.");
                }
            }
        }
    }

    private static void generateNightlyReport(Connection conn) throws SQLException {
        System.out.println("Generating Nightly Summary...");
        String query = "SELECT sum(amount) as total_volume, count(*) as tx_count FROM transactions WHERE date(transaction_date) = date('now')";
        try (PreparedStatement pstmt = conn.prepareStatement(query);
             ResultSet rs = pstmt.executeQuery()) {
            if (rs.next()) {
                System.out.println("Today's Volume: $" + rs.getDouble("total_volume"));
                System.out.println("Today's Transaction Count: " + rs.getInt("tx_count"));
            }
        }
    }
}
