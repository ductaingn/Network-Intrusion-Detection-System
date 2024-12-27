Package `kafka-python` hình như bị lỗi trên Python 3.12.

Package `cicflowmeter` bản 0.2.0 chỉ cài được trên Python 3.11 trở lên,
các bản Python bé hơn phải cài bản 0.1.6, có cấu trúc hơi khác
những gì tôi từng đọc.

Package `cicflowmeter` sử dụng các một số hàm đã bị bỏ trong `scapy==2.6.1`,
phiên bản `scapy` mới nhất hỗ trợ các hàm được sử dụng là `scapy==2.5.0`