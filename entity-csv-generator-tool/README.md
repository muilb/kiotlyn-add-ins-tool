# Entity CSV Generator Tool

A Node.js tool for automatically generating Spring Boot Entity fields from CSV file containing column definitions.

## Features

- **CSV to Entity Fields**: Converts CSV column definitions to Java entity fields
- **Smart Type Mapping**: Automatically maps SQL datatypes to Java types
- **Column Name Conversion**: Converts UPPER_SNAKE_CASE to camelCase
- **Length Support**: Handles VARCHAR(n) and other length-specified types
- **Import Detection**: Automatically detects required Java imports
- **Comment Preservation**: Includes Vietnamese field descriptions as comments

## Prerequisites

- Node.js (v14 or higher)
- npm (Node Package Manager)

## Installation

Navigate to the tool directory and install dependencies:

```bash
cd entity-csv-generator-tool
npm install
```

## CSV Format

The CSV file must follow this format (semicolon-separated):

```
Tên gợi nhớ;COLUMN_NAME;DATATYPE(LENGTH);NotNull
```

**NotNull Parameter:**
- `Yes` - Field is NOT NULL (`nullable = false`)
- `Yes(PK)` - Field is NOT NULL and Primary Key (`nullable = false`)
- Empty or any other value - Field is nullable (no nullable attribute)

### Example CSV:

```csv
Mã văn bản;ACV_TXT_CODE;VARCHAR(50);Yes
Tên văn bản;ACV_TXT_NAME;VARCHAR(255);Yes
Ngày tạo;CREATED_DATE;TIMESTAMP;Yes
Số trang;PAGE_COUNT;INT;
Số tiền;AMOUNT;DECIMAL(18,2);Yes
Trạng thái;IS_ACTIVE;BOOLEAN;
ID chính;PRIMARY_ID;BIGINT;Yes(PK)
```

## Usage

```bash
node index.js <csvFile> <outputFile>
```

### Parameters

- `<csvFile>`: Path to the input CSV file
- `<outputFile>`: Path to the output Java file

### Example

```bash
node index.js columns.csv EntityFields.java
```

## Output Format

The tool generates Java fields with this format:

```java
// Generated Entity Fields
// Date: 2025-12-12T...

// Required imports:
// import jakarta.persistence.Column;
// import java.time.LocalDateTime;
// import java.math.BigDecimal;

// Mã văn bản
@Column(name = "acvTxtCode", length = 50, nullable = false)
private String acvTxtCode;

// Tên văn bản
@Column(name = "acvTxtName", length = 255, nullable = false)
private String acvTxtName;

// Ngày tạo
@Column(name = "createdDate", nullable = false)
private LocalDateTime createdDate;

// Số trang (nullable field - no "Yes" in CSV)
@Column(name = "pageCount")
private Integer pageCount;

// Số tiền
@Column(name = "amount", nullable = false)
private BigDecimal amount;

// Trạng thái (nullable field)
@Column(name = "isActive")
private Boolean isActive;

// ID chính
@Column(name = "primaryId", nullable = false)
private Long primaryId;
```

## Datatype Mapping

The tool automatically maps SQL datatypes to Java types:

| SQL Type | Java Type |
|----------|-----------|
| VARCHAR, CHAR, TEXT, NVARCHAR | String |
| INT, INTEGER, SMALLINT | Integer |
| BIGINT, LONG | Long |
| DECIMAL, NUMERIC, NUMBER | BigDecimal |
| DATE | LocalDate |
| TIMESTAMP, DATETIME | LocalDateTime |
| TIME | LocalTime |
| BOOLEAN, BOOL, BIT | Boolean |
| FLOAT, REAL | Float |
| DOUBLE | Double |
| BLOB, BINARY | byte[] |

## Features Details

### Column Name Conversion

- `ACV_TXT_CODE` → `acvTxtCode`
- `CREATED_DATE` → `createdDate`
- `IS_ACTIVE` → `isActive`
- `USER_ID` → `userId`

### Length Handling

- `VARCHAR(50)` → `@Column(name = "...", length = 50, nullable = false)`
- `VARCHAR(255)` → `@Column(name = "...", length = 255, nullable = false)`
- `INT` → `@Column(name = "...", nullable = false)` (no length)

### Import Detection

The tool automatically detects which imports are needed:

- `BigDecimal` → adds `java.math.BigDecimal`
- `LocalDate` → adds `java.time.LocalDate`
- `LocalDateTime` → adds `java.time.LocalDateTime`
- `LocalTime` → adds `java.time.LocalTime`

## Usage in Entity Class

After generating the fields, copy and paste them into your Entity class:

```java
package jp.brycen.domain.myentity.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.LocalDateTime;
import java.math.BigDecimal;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter
@Setter
@Table(name = "my_table")
public class MyEntity {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  // Paste generated fields here
  // Mã văn bản
  @Column(name = "ACV_TXT_CODE", length = 50, nullable = false)
  private String acvTxtCode;

  // ... more fields
}
```

## CSV File Creation Tips

1. Use semicolon (`;`) as delimiter
2. No header row needed
3. Format: `Description;COLUMN_NAME;DATATYPE`
4. Column names should be in UPPER_SNAKE_CASE
5. Datatypes can include length: `VARCHAR(255)`

## Example Workflow

1. Export your database table structure to CSV
2. Format it as: `Description;COLUMN_NAME;DATATYPE(LENGTH)`
3. Run the tool: `node index.js table_columns.csv generated_fields.java`
4. Copy the generated fields to your Entity class
5. Add the required imports listed in the output

## Notes

- All fields are generated with `nullable = false` by default
- Modify the generated code if you need nullable fields
- The tool preserves Vietnamese descriptions as comments
- Column names are converted to camelCase for Java naming conventions

## Troubleshooting

If you encounter errors:

1. **CSV file not found**: Check the file path is correct
2. **Parsing errors**: Ensure CSV uses semicolon delimiter
3. **Empty output**: Check CSV has data in correct format
4. **Unknown datatype**: Tool defaults to `String` for unrecognized types

## License

ISC
