// Generated Entity Fields
// Date: 2025-12-12T04:31:19.558Z

// Required imports:
// import jakarta.persistence.Column;
// import java.math.BigDecimal;
// import java.time.LocalDate;
// import java.time.LocalDateTime;
// import java.time.LocalTime;

  // Mã văn bản
  @Column(name = "ACV_TXT_CODE", length = 50, nullable = false)
  private String acvTxtCode;

  // Tên văn bản
  @Column(name = "ACV_TXT_NAME", length = 255, nullable = false)
  private String acvTxtName;

  // Ký tự đơn
  @Column(name = "SINGLE_CHAR", length = 1)
  private String singleChar;

  // Văn bản dài
  @Column(name = "LONG_TEXT")
  private String longText;

  // Văn bản Unicode
  @Column(name = "UNICODE_NAME", length = 100)
  private String unicodeName;

  // Giá trị nhỏ
  @Column(name = "TINY_VALUE", nullable = false)
  private int tinyValue;

  // Số nguyên
  @Column(name = "COUNT_VALUE")
  private Integer countValue;

  // Số nguyên nhỏ
  @Column(name = "SMALL_NUMBER")
  private Integer smallNumber;

  // Số nguyên lớn
  @Column(name = "BIG_NUMBER", nullable = false)
  private Long bigNumber;

  // Số thực
  @Column(name = "DECIMAL_VALUE", nullable = false)
  private BigDecimal decimalValue;

  // Số thực chính xác
  @Column(name = "NUMERIC_VALUE")
  private BigDecimal numericValue;

  // Số đơn
  @Column(name = "NUMBER_FIELD")
  private BigDecimal numberField;

  // Ngày sinh
  @Column(name = "BIRTH_DATE")
  private LocalDate birthDate;

  // Ngày tạo
  @Column(name = "CREATED_DATE", nullable = false)
  private LocalDateTime createdDate;

  // Ngày cập nhật
  @Column(name = "UPDATED_AT")
  private LocalDateTime updatedAt;

  // Giờ làm việc
  @Column(name = "WORK_TIME")
  private LocalTime workTime;

  // Trạng thái kích hoạt
  @Column(name = "IS_ACTIVE")
  private Boolean isActive;

  // Đã xóa
  @Column(name = "IS_DELETED")
  private Boolean isDeleted;

  // Bit cờ
  @Column(name = "FLAG_BIT")
  private Boolean flagBit;

  // Số thực đơn
  @Column(name = "FLOAT_VALUE")
  private Float floatValue;

  // Số thực kép
  @Column(name = "DOUBLE_VALUE")
  private Double doubleValue;

  // Tỷ lệ thực
  @Column(name = "RATE_REAL")
  private Float rateReal;

  // Dữ liệu nhị phân
  @Column(name = "BINARY_DATA")
  private byte[] binaryData;

  // File nhị phân
  @Column(name = "FILE_CONTENT")
  private byte[] fileContent;

  // Người tạo ID
  @Column(name = "CREATED_BY_ID", nullable = false)
  private Long createdById;

  // Mô tả chi tiết
  @Column(name = "DESCRIPTION")
  private String description;
