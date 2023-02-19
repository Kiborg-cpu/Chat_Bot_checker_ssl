import socket
from urllib.parse import urlparse

import OpenSSL
import ssl

import certifi


class SSLUtils:
    @staticmethod
    def pem_to_x509(cert_data: str):
        """Converts a given pem encoded certificate to X509 object
        @param cert_data: str pem encoded certificate data that includes the header and footer
        @return: X509 object
        """
        return OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, str.encode(cert_data))

    def fetch_server_certificate(self, dns_name: str, port: int):
        """Fetch the server certificate from the given dns_name and port
        @param dns_name: The dns name to fetch the certificate for
        @param port: The port that is serving the certificate
        @return: X509 certificate object
        """
        pem_server_certificate = ssl.get_server_certificate((dns_name, port))
        x509_server_certificate = self.pem_to_x509(pem_server_certificate)
        return x509_server_certificate

    def fetch_server_certificate_sni(self, dns_name: str, port: int):
        """Fetch the server certificate from the given dns_name and port
           This implementation supports SNI. Compare to ssl.get_server_certificate() which will return an incorrect
           cert if SNI is enabled on the server
        @param dns_name: The dns name to fetch the certificate for
        @param port: The port that is serving the certificate
        @return: X509 certificate object
        """
        connection = ssl.create_connection((dns_name, port))
        context = ssl.SSLContext()
        sock = context.wrap_socket(connection, server_hostname=dns_name)
        server_certificate = self.pem_to_x509(ssl.DER_cert_to_PEM_cert(sock.getpeercert(True)))
        sock.close()
        return server_certificate

    def fetch_sever_sertificate_x509(self, dns_name: str):
        parsed = dns_name
        if 'http' in dns_name:
            parsed = urlparse(dns_name)
            parsed = parsed.netloc
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            conn = context.wrap_socket(socket.socket(socket.AF_INET),
                                       server_hostname=parsed)
            context.load_verify_locations(certifi.where())
            print('parsed:', parsed)
            conn.connect((parsed, 443))
            #ssl.get_server_certificate((parsed, 443))
            cert = conn.getpeercert()
            return cert
        except Exception:
            return None

# tool = SSLUtils()
###cert = tool.fetch_server_certificate_sni('google.com', 443)
# cert = tool.fetch_sever_sertificate_no_x509('google.com')
# pprint.pprint(cert)
##print(cert.items())
