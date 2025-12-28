### Finance Upload File Structure

To process payment updates, upload an Excel (`.xlsx`, `.xls`) or CSV (`.csv`) file. The system allows you to map columns after uploading, but using the recommended structure ensures smoother processing.

#### Recommended Column Structure

| Column Name | Description | Required? | Example |
| :--- | :--- | :--- | :--- |
| **Student ID** | The unique registration number or ID of the student. This is the primary key for matching records. | **Yes** | `2023-B291-10023` |
| **Student Name** | Full name of the student. Used for verification (optional but recommended). | No | `John Doe` |
| **Amount Paid** | The amount paid in the currency (e.g., UGX). | No | `600000` |
| **Payment Date** | Date of the transaction (Format: `YYYY-MM-DD` or `DD/MM/YYYY`). | No | `2024-02-15` |
| **Meal Plan** | Specifies if payment is for `Full Day`, `Lunch`, `Supper`, etc. | No | `Full Day` |
| **Semester** | The academic semester this payment applies to. | No | `Semester 1 2024/2025` |
| **Status** | Explicit status if available (e.g., `Paid`). If blank, the system may infer based on amount. | No | `Paid` |

#### Validation Rules
1.  **Student ID**: Must match an existing user in the system. If not found, the record will be flagged as "Invalid".
2.  **Duplicate Entries**: If the same Student ID appears multiple times in the file, it will be flagged for review.
3.  **Ambiguity**: Ensure columns are clearly labeled to make the mapping step easier.
