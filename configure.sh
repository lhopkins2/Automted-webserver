echo '<html>' > index.html
echo 'Private IP address: ' >> index.html
curl http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html
echo '<br> Local Hostname: ' >> index.html
curl http://169.254.169.254/latest/meta-data/local-hostname >> index.html
echo '<br> Instance Type: ' >> index.html
curl http://169.254.169.254/latest/meta-data/instance-type >> index.html
echo '<br>The requested image: <br>"' >> index.html
echo '<img src="https://s3-eu-west-1.amazonaws.com/lhopkinsbucket2021/image.jpg">' >> index.html
sudo cp index.html /var/www/html/index.html
