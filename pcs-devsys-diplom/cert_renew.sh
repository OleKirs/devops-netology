#!/usr/bin/env bash
# Renew cert for test.local
# Prereqs: Hasicorp Vault, NGINX, OpenSSL, JQ

# Vars

VAULT_TOKEN='s.BnJd5fmY8dF3ZSnIYutVsScv'
cert_file_name='test.local.cert.pem'
site_ssl_dir='/etc/nginx/ssl/test.local'

# Funcs
function create_new_cert() {
  vault write -format=json pki_int/issue/test-dot-local \
    format=pem_bundle \
    common_name="test.local" \
    alt_names="test.local,www.test.local,netology.test.local" \
    ttl="720h" | jq -r '.data.certificate' >$1
  echo "Check 1"
}

#MAIN
site_cert_full_path="$site_ssl_dir/$cert_file_name"

# Check vault is sealed
seal_vault=$(vault status)
if grep -q 'Sealed             true' <<<$seal_vault; then
  echo 'ERROR: VAULT SEALED' >&2
  exit 50
fi

# Login into vault with root creds
vault login $VAULT_TOKEN &>/dev/null
if [ $? != 0 ]; then
  echo "Can\`t login into vault: $?" >&2
  exit 51
fi

# Revoke & delete old cert
cert_sn=$(openssl x509 -noout -serial -in test.local.cert.pem)        # Get SN from current cert
cert_serial_number=$(sed 's/.*=//g;s/../&:/g;s/:$//' <<<$cert_sn)     # Convert SN to xx:xx view
vault write pki_int/revoke serial_number="$cert_serial_number"        # Revoke cert w SN
vault write pki_int/tidy tidy_cert_store=true tidy_revoked_certs=true # Delete revoked certs

# Request new certificates
create_new_cert $cert_file_name

# Place new cert into site SSL dir
cp $cert_file_name $site_cert_full_path

# Restart NGINX to commit changes
systemctl restart nginx

echo 'All done'

exit 0
EOF
