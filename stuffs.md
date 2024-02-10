## O que tive que fazer:

- Atualizar o local.conf e o bblayers.conf
- Adicionar servers no ntp.conf
- Subir manualmente o openvpn: openvpn --config /etc/openvpn/client/edge-client.conf --dev tun0 --cert /etc/openvpn/client/edge-client.crt --key /etc/openvpn/client/edge-client.key --tls-auth /etc/openvpn/client/ta.key --askpass /etc/openvpn/client/edge-client.pass --ca /etc/openvpn/client/ca.crt &


## Instalar:
```
sudo chmod +x setup-external-deps.sh
./setup-external-deps.sh 
apagar ./yocto/build/conf/templateconf.cfg
docker build -t yocto-raspberry-4_yocto .

```
## Para rodar:
```
docker run -v ~/Projects/yocto-raspberry-4/yocto:/home/yocto -it  yocto-raspberry-4_yocto /bin/bash
. sources/poky/oe-init-build-env
bitbake core-image-base
```
## ssh:
```
ssh root@pingu.local
```


### PWD Generate:
```
mkpasswd -m sha-512 chatuba -s "11223344"
```
(precisa colocar `\` sempre quando tiver um `$`)

