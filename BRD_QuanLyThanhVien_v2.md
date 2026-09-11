# BRD: Quản lý Thành viên Doanh nghiệp

**Version:** 1.0
**Ngày:** 2026-09-11
**Author:** BA Agent (theo yêu cầu tuyetlp@cas.so)
**Status:** Draft

---

## 1. Mục tiêu & Bối cảnh

### 1.1 Vấn đề hiện tại (AS-IS)

Sau khi một doanh nghiệp được xác thực trên Cas ID, chỉ duy nhất người đã thực hiện xác thực (giám đốc /
người đại diện pháp luật) mới có quyền thao tác trên toàn bộ tài sản số của doanh nghiệp — đăng ký/tạm dừng
tài khoản ngân hàng, đăng ký/ký chứng thư số, đăng ký/cấp quyền hóa đơn điện tử, đăng nhập định danh QR.

Trên thực tế, giám đốc không phải lúc nào cũng trực tiếp vận hành các nghiệp vụ này. Công việc vận hành
thường được giao cho kế toán trưởng hoặc người quản lý được tin tưởng, trong khi giám đốc chỉ giữ vai trò
tham mưu và phê duyệt những việc thực sự quan trọng. Hệ thống hiện tại không có cơ chế nào để giám đốc san
sẻ quyền thao tác này một cách có kiểm soát — mọi việc đều phải qua đúng một tài khoản.

### 1.2 Mục tiêu kỳ vọng (TO-BE)

Giám đốc có thể mời thêm các cá nhân khác (đã có tài khoản Cas ID) tham gia làm thành viên của doanh nghiệp,
và cấp cho mỗi người một tập quyền vận hành cụ thể theo từng loại tài sản — thay vì phải cho toàn quyền.
Người được mời phải tự xác nhận đồng ý trước khi quyền có hiệu lực. Giám đốc (hoặc người được giao quyền
tương đương) luôn có thể xem lại, điều chỉnh hoặc thu hồi quyền của từng thành viên bất kỳ lúc nào, và mọi
hành động trên doanh nghiệp đều ghi nhận được người thực hiện.

**Đo lường thành công:**
- Một doanh nghiệp có thể có nhiều hơn 1 người thao tác được tài sản, mỗi người chỉ thấy/dùng được đúng
  phần quyền đã được cấp.
- Không có thành viên nào có quyền truy cập tài sản mà chưa tự xác nhận đồng ý tham gia.
- Giám đốc không thể bị gỡ khỏi danh sách thành viên trong bất kỳ trường hợp nào.

### 1.3 Lý do thực hiện

Business driver: giảm sự phụ thuộc vào một cá nhân duy nhất (giám đốc) trong vận hành tài sản số, cho phép
phân công công việc đúng người đúng việc, đồng thời vẫn giữ được khả năng kiểm soát và truy vết trách nhiệm
(ai làm gì, khi nào) — chuẩn bị nền tảng cho yêu cầu tuân thủ nội bộ (audit) ở các giai đoạn sau.

---

## 2. Phạm vi (Scope)

### Trong phạm vi

- Thêm thành viên mới bằng cách tra cứu theo số CCCD (thành viên phải đã có tài khoản Cas ID).
- Gán vai trò hiển thị (Giám đốc, Kế toán trưởng, Kế toán viên, Nhân viên...) và phân quyền theo **5 nhóm
  quyền**: Ngân hàng, Chứng thư số, Hóa đơn, Định danh, và **Quản lý thành viên** (nhóm mới).
- Luồng lời mời — xác nhận: thành viên được mời phải tự Chấp nhận hoặc Từ chối từ tài khoản của chính họ.
- 3 trạng thái thành viên: Chờ xác nhận, Đã tham gia, Từ chối.
- Gỡ thành viên đã tham gia; thu hồi lời mời đang chờ hoặc đã bị từ chối — chỉ thực hiện được bởi người có
  quyền "Quản lý thành viên".
- Ràng buộc: giám đốc (người xác thực doanh nghiệp) không thể bị gỡ.
- Trang chủ của thành viên phản ánh đúng và chỉ đúng những gì họ được cấp quyền: doanh nghiệp không hiện
  hồ sơ cho đến khi tự xác nhận tham gia; sau khi tham gia, chỉ các mục tài sản được cấp quyền mới mở khóa.
- Ghi nhận (ở mức yêu cầu) rằng mọi hành động trên doanh nghiệp cần lưu vết người thao tác.

### Ngoài phạm vi (Out of Scope)

- Thành viên tự rời khỏi doanh nghiệp (không có hành động "rời nhóm" cho chính mình).
- Màn hình xem/tra cứu lịch sử log chi tiết và cơ chế lưu trữ log — sẽ thiết kế ở một BRD/FRD riêng sau này;
  tài liệu này chỉ ghi nhận đây là một yêu cầu cần chuẩn bị nền tảng dữ liệu.
- Giới hạn số lượng thành viên tối đa trên một doanh nghiệp.
- Phân cấp nhiều tầng vai trò quản trị (ví dụ "Phó giám đốc" với quyền hạn riêng biệt so với "Kế toán
  trưởng được cấp quyền quản lý thành viên") — hiện tại quyền hạn hoàn toàn do tập phân quyền quyết định,
  không có khái niệm cấp bậc.

---

## 3. Stakeholders

| Vai trò | Tên/Team | Trách nhiệm |
|---|---|---|
| Product Owner | tuyetlp@cas.so | Duyệt yêu cầu nghiệp vụ |
| Giám đốc doanh nghiệp (Primary Actor) | Chủ tài khoản Cas ID đã xác thực doanh nghiệp | Mời thành viên, phân quyền, gỡ/thu hồi |
| Thành viên được cấp quyền "Quản lý thành viên" (Primary Actor) | Kế toán trưởng / người quản lý được ủy quyền | Thực hiện thay giám đốc: thêm, gỡ, thu hồi thành viên |
| Thành viên vận hành (Actor) | Kế toán trưởng, Kế toán viên, Nhân viên... | Thao tác tài sản trong phạm vi quyền được cấp |
| Đội vận hành Cas ID | CS Cas ID | Hỗ trợ xử lý khiếu nại/lỗi liên quan |
| Dev Team | Đội phát triển Cas ID | Triển khai |

---

## 4. Yêu cầu nghiệp vụ

> Dùng từ khóa: **Shall** (bắt buộc) / **Should** (khuyến nghị) / **May** (tùy chọn)

### BR-01: Giám đốc là thành viên mặc định, Toàn quyền, không thể bị gỡ

- **Mô tả:** Ngay khi doanh nghiệp được xác thực thành công, hệ thống shall tự động thêm người đã xác thực
  (giám đốc) vào danh sách thành viên với trạng thái "Đã tham gia" và quyền "Toàn quyền", không cần thao tác
  thủ công.
- **Lý do:** Giám đốc là người chịu trách nhiệm pháp lý cao nhất, luôn phải có mặt và có đầy đủ quyền hạn.
- **Tiêu chí thành công:** Mọi doanh nghiệp đã xác thực đều có ít nhất 1 thành viên (giám đốc) ở trạng thái
  Đã tham gia ngay khi mở màn Quản lý thành viên lần đầu.

### BR-02: Thêm thành viên mới qua tra cứu CCCD

- **Mô tả:** Người có quyền "Quản lý thành viên" shall có thể thêm một thành viên mới bằng cách nhập số
  CCCD; hệ thống tự động tìm và hiển thị đúng hồ sơ Cas ID tương ứng (tên, ảnh đại diện) nếu tồn tại.
- **Lý do:** Đảm bảo chỉ những cá nhân đã có tài khoản Cas ID thật mới được mời, tránh nhập sai thông tin thủ công.
- **Tiêu chí thành công:** Nhập đúng CCCD đã đăng ký Cas ID → hệ thống hiển thị đúng hồ sơ; nhập CCCD không
  tồn tại hoặc sai định dạng → hệ thống báo lỗi rõ ràng, không cho tiếp tục.

### BR-03: Phân quyền theo 5 nhóm quyền

- **Mô tả:** Khi thêm hoặc chỉnh sửa một thành viên, hệ thống shall cho phép chọn "Tất cả (Toàn quyền)" hoặc
  tick riêng từng quyền trong 5 nhóm: (1) Ngân hàng — Đăng ký mới / Tạm dừng / Cấp quyền ứng dụng (có chọn
  cụ thể từng tài khoản ngân hàng); (2) Chứng thư số — Đăng ký mới-Gia hạn / Ký số; (3) Hóa đơn — Đăng ký /
  Cấp quyền; (4) Định danh — Đăng nhập QR; (5) **Quản lý thành viên — Thêm thành viên / Xóa thành viên**.
- **Lý do:** Nhóm quyền thứ 5 tách biệt hoàn toàn khỏi quyền tài sản, để giám đốc có thể giao việc quản lý
  nhân sự nội bộ cho một người mà không bắt buộc phải cho họ toàn quyền thao tác tài sản.
- **Tiêu chí thành công:** Một thành viên chỉ được cấp nhóm quyền 5 (không có quyền tài sản nào khác) vẫn
  có thể thêm/xóa thành viên khác, nhưng không thao tác được bất kỳ tài sản nào.

### BR-04: Lời mời phải được thành viên tự xác nhận

- **Mô tả:** Sau khi được thêm, thành viên mới shall ở trạng thái "Chờ xác nhận" và KHÔNG có quyền thao tác
  gì cho đến khi tự đăng nhập vào tài khoản Cas ID của chính họ và chọn "Chấp nhận". Màn xác nhận shall hiển
  thị: tên doanh nghiệp, người mời, vai trò được đề nghị, và tóm tắt quyền được cấp.
- **Lý do:** Không ai được gán trách nhiệm/quyền hạn trên tài sản doanh nghiệp mà chưa đồng ý.
- **Tiêu chí thành công:** Trước khi xác nhận, trang chủ của thành viên không hiển thị hồ sơ doanh nghiệp
  này; hệ thống hiện banner nhắc "Bạn được mời tham gia N doanh nghiệp" và số thông báo chưa đọc tương ứng.

### BR-05: Từ chối lời mời

- **Mô tả:** Thành viên được mời shall có thể chọn "Từ chối" thay vì "Chấp nhận" ngay tại màn xác nhận.
- **Lý do:** Tôn trọng quyền quyết định của người được mời.
- **Tiêu chí thành công:** Sau khi từ chối, thành viên chuyển sang trạng thái "Từ chối"; phía giám đốc/người
  quản lý thấy rõ trạng thái này trong danh sách thành viên.

### BR-06: Gỡ thành viên đã tham gia

- **Mô tả:** Người có quyền "Quản lý thành viên" shall có thể gỡ một thành viên đang ở trạng thái "Đã tham
  gia" ra khỏi doanh nghiệp, thu hồi toàn bộ quyền thao tác của người đó ngay lập tức.
- **Lý do:** Hỗ trợ trường hợp thành viên nghỉ việc, đổi vai trò, hoặc không còn cần quyền truy cập.
- **Tiêu chí thành công:** Sau khi bị gỡ, thành viên không còn thấy hồ sơ doanh nghiệp này trên trang chủ
  của họ.

### BR-07: Thu hồi lời mời (Chờ xác nhận / Từ chối)

- **Mô tả:** Người có quyền "Quản lý thành viên" shall có thể thu hồi một lời mời đang ở trạng thái "Chờ
  xác nhận" (hủy trước khi người kia phản hồi), hoặc xóa khỏi danh sách một người đã "Từ chối".
- **Lý do:** Tránh tồn đọng những lời mời không còn cần thiết hoặc đã bị từ chối trong danh sách quản lý.
- **Tiêu chí thành công:** Sau khi thu hồi lời mời đang chờ, thông báo mời tương ứng phía người được mời
  không còn hiệu lực (không thể Chấp nhận nữa).

### BR-08: Giám đốc không thể bị gỡ; thành viên không tự rời

- **Mô tả:** Hệ thống shall chặn hành động gỡ đối với thành viên có vai trò Giám đốc, bất kể ai đang thao
  tác. Hệ thống shall not cung cấp hành động "rời doanh nghiệp" cho chính thành viên tự thực hiện — việc gỡ
  chỉ được khởi tạo bởi người có quyền "Quản lý thành viên".
- **Lý do:** Giám đốc là người chịu trách nhiệm pháp lý, không được để doanh nghiệp rơi vào trạng thái không
  có người đại diện quản lý.
- **Tiêu chí thành công:** Nút/hành động gỡ không xuất hiện (hoặc bị vô hiệu hóa) khi mục tiêu là thành viên
  vai trò Giám đốc.

### BR-09: Ghi nhận log thao tác trên doanh nghiệp

- **Mô tả:** Hệ thống should ghi nhận người thực hiện cho mọi hành động liên quan đến doanh nghiệp (thêm/gỡ
  thành viên, thay đổi phân quyền, và về sau là các thao tác trên tài sản).
- **Lý do:** Chuẩn bị nền tảng cho yêu cầu truy vết trách nhiệm (audit) khi nhiều người cùng thao tác trên
  một doanh nghiệp.
- **Tiêu chí thành công:** [TBD - cơ chế lưu trữ, định dạng và màn hình hiển thị log sẽ được đặc tả trong
  BRD/FRD riêng ở giai đoạn sau; lần này chỉ yêu cầu dữ liệu nghiệp vụ (ai, hành động gì, thời điểm nào)
  không bị mất khi các hành động ở BR-02, 06, 07 xảy ra].

### BR-10: Trang chủ phản ánh đúng quyền hạn thực tế

- **Mô tả:** Trên trang chủ của một thành viên, mỗi mục tài sản (Ngân hàng, Chứng thư số, Hóa đơn, Định
  danh) shall chỉ mở khóa nếu thành viên đó có ít nhất một quyền liên quan trong nhóm tương ứng (hoặc Toàn
  quyền); nếu không, mục đó hiển thị ở trạng thái khóa.
- **Lý do:** Đảm bảo giao diện không gây hiểu lầm về quyền hạn thực tế của người dùng.
- **Tiêu chí thành công:** Một thành viên chỉ được cấp quyền "Ngân hàng: Đăng ký mới" thấy đúng 1 mục Ngân
  hàng mở khóa, các mục còn lại (Chứng thư số, Hóa đơn, Định danh) vẫn khóa.

---

## 5. Ràng buộc & Rủi ro

### Ràng buộc

- **Nghiệp vụ:** Thành viên phải đã có tài khoản Cas ID từ trước (được định danh bằng CCCD) — hệ thống
  không hỗ trợ mời người chưa có tài khoản.
- **Nghiệp vụ:** Không có khái niệm phân cấp vai trò quản trị nhiều tầng — quyền hạn hoàn toàn do 5 nhóm
  quyền quyết định, không phải do "chức danh" hiển thị.
- **Kỹ thuật:** Cơ chế log chi tiết (BR-09) chưa có đặc tả kỹ thuật đầy đủ trong tài liệu này — cần một
  FRD riêng trước khi triển khai.

### Rủi ro

| Rủi ro | Xác suất | Mức độ | Mitigation |
|---|---|---|---|
| Người được cấp quyền "Quản lý thành viên" lạm dụng, gỡ hàng loạt thành viên khác | Thấp | Cao | Ghi log đầy đủ (BR-09) để truy vết; cân nhắc thêm xác nhận 2 bước khi gỡ ở giai đoạn sau |
| Thành viên bị gỡ nhầm trong khi đang thao tác dở dang trên tài sản | Trung bình | Trung bình | Thông báo cho thành viên ngay khi bị gỡ; các thao tác dở dang cần được xử lý ở tầng nghiệp vụ tài sản tương ứng |
| Không phân biệt được ai chịu trách nhiệm cuối cùng khi nhiều thành viên cùng có quyền trên một tài sản | Trung bình | Trung bình | Ưu tiên triển khai BR-09 (log) sớm ở giai đoạn kế tiếp |

---

## 6. Tiêu chí chấp thuận (Acceptance Criteria)

- [ ] **Given** doanh nghiệp vừa xác thực xong, **When** giám đốc mở màn Quản lý thành viên lần đầu, **Then**
      giám đốc đã có sẵn trong danh sách với trạng thái Đã tham gia và Toàn quyền.
- [ ] **Given** người có quyền Quản lý thành viên nhập đúng CCCD của một tài khoản Cas ID đang tồn tại,
      **When** họ chọn vai trò + phân quyền và gửi lời mời, **Then** thành viên mới xuất hiện ở trạng thái
      Chờ xác nhận, và người được mời nhận được thông báo tương ứng trên tài khoản của chính họ.
- [ ] **Given** một thành viên đang Chờ xác nhận, **When** họ mở thông báo và chọn Chấp nhận, **Then** hồ sơ
      doanh nghiệp xuất hiện trên trang chủ của họ, đúng các mục tài sản đã được cấp quyền mở khóa.
- [ ] **Given** một thành viên đang Chờ xác nhận, **When** họ chọn Từ chối, **Then** trạng thái chuyển thành
      Từ chối và họ không có quyền gì trên doanh nghiệp.
- [ ] **Given** người có quyền Quản lý thành viên xem danh sách thành viên, **When** họ chọn gỡ một thành
      viên Đã tham gia, **Then** thành viên đó mất toàn bộ quyền ngay lập tức.
- [ ] **Given** danh sách thành viên có người đang Chờ xác nhận hoặc đã Từ chối, **When** người có quyền
      Quản lý thành viên chọn thu hồi, **Then** lời mời/bản ghi đó không còn hiệu lực.
- [ ] **Given** danh sách thành viên có Giám đốc, **When** bất kỳ ai (kể cả người có quyền Quản lý thành
      viên) cố gắng gỡ Giám đốc, **Then** hành động bị chặn.
- [ ] **Given** một thành viên đã Đã tham gia, **Then** không có hành động "Rời doanh nghiệp" nào khả dụng
      cho chính họ tự thực hiện.
