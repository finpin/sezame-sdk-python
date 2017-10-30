from OpenSSL import crypto, SSL


class CertUtil:
    @staticmethod
    def make_csr(clientcode, email='', country_name='AT'):
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        req = crypto.X509Req()
        req.get_subject().CN = clientcode
        if len(email) > 0:
            req.get_subject().emailAddress = email
        req.get_subject().countryName = country_name
        req.get_subject().stateOrProvinceName = '-'
        req.get_subject().localityName = '-'
        req.get_subject().organizationName = '-'
        req.get_subject().organizationalUnitName = '-'

        req.set_pubkey(key)
        req.sign(key, "sha256")

        private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode(encoding='UTF-8')
        csr = crypto.dump_certificate_request(crypto.FILETYPE_PEM, req).decode(encoding='UTF-8')

        return private_key, csr
