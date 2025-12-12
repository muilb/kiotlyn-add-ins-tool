// Generated Entity Fields
// Date: 2025-12-12T04:30:22.940Z

// Required imports:
// import jakarta.persistence.Column;
// import java.time.LocalDateTime;
// import java.math.BigDecimal;

  // Mã văn bản
  @Column(name = "ACV_TXT_CODE", length = 50, nullable = false)
  private String acvTxtCode;

  // Tên văn bản
  @Column(name = "ACV_TXT_NAME", length = 255, nullable = false)
  private String acvTxtName;

  // Ngày tạo
  @Column(name = "CREATED_DATE", nullable = false)
  private LocalDateTime createdDate;

  // Số trang
  @Column(name = "PAGE_COUNT")
  private Integer pageCount;

  // Số tiền
  @Column(name = "AMOUNT", nullable = false)
  private BigDecimal amount;

  // Trạng thái kích hoạt
  @Column(name = "IS_ACTIVE")
  private Boolean isActive;

  // Mô tả chi tiết
  @Column(name = "DESCRIPTION")
  private String description;

  // Người tạo ID
  @Column(name = "CREATED_BY_ID", nullable = false)
  private Long createdById;

  // Ngày cập nhật
  @Column(name = "UPDATED_AT")
  private LocalDateTime updatedAt;

  // Tỷ lệ phần trăm
  @Column(name = "PERCENTAGE")
  private BigDecimal percentage;
