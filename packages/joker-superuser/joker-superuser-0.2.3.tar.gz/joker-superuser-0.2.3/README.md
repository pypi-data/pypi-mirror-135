joker-superuser
===============

### Miscellaneous 

Get resources with SVN:

    svn export https://github.com/frozflame/joker-superuser/trunk/resources sus-resources
    
Get resources with curl and tar:
   
    mkdir sus-resources
    curl -L "https://github.com/frozflame/joker-superuser/archive/master.tar.gz" | tar xz -C sus-resources --strip-components 2 joker-superuser-master/resources/ 
