import socket
import argparse


def validate_hostname(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror:
        return None


def determine_protocol(hostname, port):
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(5)
        tcp_socket.connect((hostname, port))
        tcp_socket.close()
        return "TCP"
    except (socket.timeout, ConnectionRefusedError):
        pass

    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.settimeout(5)
        udp_socket.sendto(b"", (hostname, port))
        udp_socket.close()
        return "UDP"
    except (socket.timeout, ConnectionRefusedError):
        pass

    return "Unknown"


def check_service_status(hostname, port):
    ip_address = validate_hostname(hostname)
    if ip_address is None:
        return None, None

    protocol = determine_protocol(hostname, port)

    try:
        if protocol == "TCP":
            socket_type = socket.SOCK_STREAM
        elif protocol == "UDP":
            socket_type = socket.SOCK_DGRAM
        else:
            return ip_address, None

        test_socket = socket.socket(socket.AF_INET, socket_type)
        test_socket.settimeout(5)
        test_socket.connect((hostname, port))
        test_socket.close()
        return ip_address, protocol
    except (socket.timeout, ConnectionRefusedError):
        return ip_address, None
    except Exception:
        return ip_address, None


def parse_arguments():
    parser = argparse.ArgumentParser(description='Service Status Checker')
    parser.add_argument('hostname', type=str, help='hostname to check')
    parser.add_argument('port', type=int, help='port number to check')
    return parser.parse_args()


def main():
    args = parse_arguments()
    hostname = args.hostname
    port = args.port

    ip_address, protocol = check_service_status(hostname, port)
    if ip_address is None:
        print(f"主机名验证失败: {hostname}")
    else:
        print(f"主机名验证成功，IP地址: {ip_address}")

        if protocol is None:
            print("无法确定可用的协议")
            print("服务未开启")
        else:
            print(f"{protocol}协议可用")
            print("服务可用")


if __name__ == '__main__':
    main()
