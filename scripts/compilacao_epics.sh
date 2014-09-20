#!/bin/bash

# Para voce conseguir rodar o elegant e os arquivos do SDDS corretamente
# na sua area, ou então para reinstalar o elegant, edite seu arquivo .bashrc
# adicionando no final do arquivo as seguintes linhas:
#export PATH=/usr/local/epics_oag/epics/base/bin/linux-x86_64:/usr/local/epics_oag/epics/extensions/bin/linux-x86_64:/usr/local/epics_oag/oag/apps/bin/linux-x86_64:/usr/local/mpich-install/bin:$PATH:.

#export TCLLIBPATH="/usr/local/epics_oag/oag/apps/lib/linux-x86_64 /usr/local/epics_oag/epics/extensions/lib/linux-x86_64"
#export PYTHONPATH=$PYTHONPATH:/usr/local/epics_oag/oag/apps/lib/linux-x86_64:/usr/local/epics_oag/epics/extensions/lib/linux-x86_64

#export RPN_DEFNS=/usr/local/epics_oag/defns.rpn
#export HOST_ARCH=linux-x86_64
#export EPICS_HOST_ARCH=linux-x86_64
#export OAG_TOP_DIR=/usr/local/epics_oag

# mude as permissoes da pasta:
sudo mkdir /usr/local/epics_oag || return
sudo chown fernando.fac /usr/local/epics_oag || return


# entre na pasta /usr/local/epics_oag e exclua tudo o que estiver la dentro
cd /usr/local/epics_oag || return
rm -rf * || return

# faca o download dos arquivos necessarios.
# na minha pasta /home/fernando/codigos_dinamica_feixes/SDDS_elegant_source ja tem uma versao desses arquivos:
#    SDDS.3.2.tar.gz
#    SDDSepics.3.2.tar.gz
#    baseR3.14.12.4.tar.gz
#    elegant.26.0.2.tar.gz
#    epics.extensions.configure.tar.gz
#    oag.apps.configure.tar.gz
#    oag.1.21.tar.gz
#    defns.rpn
# verifique no site do anl se há versões mais novas desses arquivos e os atualize

# copie or arquivos *.tar.gz para dentro da pasta /usr/local/epics_oag
scp fernando-linux:/home/fernando/codigos_dinamica_feixes/Moga-SDDS-Elegant/{*.gz,defns.rpn} /usr/local/epics_oag/ || return

# descomprima o arquivo "baseR3.14.12.4.tar.gz" com: 
tar -zxvf baseR3.14.12.4.tar.gz  || return
# isso criara uma pasta "base-3.14.12.4".
# Agora descomprima as extensões do epics:
tar -zxvf epics.extensions.configure.tar.gz || return
# Agora, descomprima os arquivos:
tar -zxvf SDDS.3.2.tar.gz && tar -zxvf SDDSepics.3.2.tar.gz \
&& tar -zxvf oag.apps.configure.tar.gz && tar -zxvf elegant.26.0.2.tar.gz \
&& tar -zxvf oag.1.21.tar.gz  || return

#Crie a seguinte pasta:
mkdir -p epics/base  || return
# mova tudo o que esta em "base-3.14.12.4" para dentro dela:
mv base-3.14.12.4/* epics/base/  || return
# e apague a pasta original:
rmdir base-3.14.12.4/  || return

# agora, abra os arquivos
#gedit epics/base/configure/CONFIG epics/extensions/configure/CONFIG &
# e adicione as seguintes linhas no final dele:
#CROSS_COMPILER_TARGET_ARCHS=
#SHARED_LIBRARIES=YES
#STATIC_BUILD=YES
# O comando abaixo faz isso:
#var='CROSS_COMPILER_TARGET_ARCHS='
#cat epics/base/configure/CONFIG | sed -e "s/$var*/$var/g" \
#> epics/base/configure/CONFIG2 && mv epics/base/configure/CONFIG{2,}  || return
#cat epics/extensions/configure/CONFIG | sed -e "s/$var*/$var/g" \
#> epics/extensions/configure/CONFIG2 && mv epics/extensions/configure/CONFIG{2,}  || return
echo ' ' >> epics/base/configure/CONFIG
echo ' ' >> epics/extensions/configure/CONFIG 
echo 'CROSS_COMPILER_TARGET_ARCHS=' >> epics/base/configure/CONFIG
echo 'CROSS_COMPILER_TARGET_ARCHS=' >> epics/extensions/configure/CONFIG 
echo 'SHARED_LIBRARIES = YES' >> epics/base/configure/CONFIG
echo 'SHARED_LIBRARIES = YES' >> epics/extensions/configure/CONFIG 
echo 'STATIC_BUILD = YES' >> epics/base/configure/CONFIG
echo 'STATIC_BUILD = YES' >> epics/extensions/configure/CONFIG 

#var='SHARED_LIBRARIES=YES'
#cat epics/base/configure/CONFIG | sed -e "s/${var}.*/${var}YES/g" \
#> epics/base/configure/CONFIG2 && mv epics/base/configure/CONFIG{2,}  || return
#cat epics/extensions/configure/CONFIG | sed -e "s/${var}.*/${var}YES/g" \
#> epics/extensions/configure/CONFIG2 && mv epics/extensions/configure/CONFIG{2,}  || return

# Agora, provavelmente, voce tera que instalar algumas bibliotecas para
# o epics e suas extensoes compilarem corretamente:
sudo apt-get install libreadline6-dev libncurses5-dev libncursesw5-dev \
zlib1g-dev libgd2-xpm-dev libxaw7-dev liblapack-dev libmotif-dev libgsl0-dev \
 python-dev iwidgets4 tcl8.5 tk8.5 tcl8.5-dev tk8.5-dev mpich2  || return

sudo apt-get remove tcl8.6 tcl8.6-dev tk8.6 tk8.6-dev
sudo ln -s /usr/bin/tclsh{8.5,}

# tambem eh necessario ter instalados o g++ e o gfortran

# Se a instalacao de apenas essas bibliotecas não for suficiente, olhe o endereço:
# https://wiki.lnls.br/mediawiki/index.php/SOL:Instala%C3%A7%C3%A3o_da_base_EPICS_Linux
# Nele há uma lista de bibliotecas necessarias para instalar o epics

# agora, compile o epics:
cd epics/base && make && cd -  || return


# Abra o arquivo:
#gedit /usr/local/epics_oag/epics/extensions/configure/os/CONFIG_SITE.linux-x86_64.linux-x86_64 &
# E altere o caminho das bibliotecas:
#X11_LIB=/usr/lib/x86_64-linux-gnu
#MOTIF_LIB=/usr/lib/x86_64-linux-gnu
# O comando abaixo faz isso:
X11='X11_LIB='
MOTIF='MOTIF_LIB='
cat /usr/local/epics_oag/epics/extensions/configure/os/CONFIG_SITE.linux-x86_64.linux-x86_64 \
   | sed "s/${X11}.*/${X11}\/usr\/lib\/x86_64-linux-gnu/g" | sed "s/${MOTIF}.*/${MOTIF}\/usr\/lib\/x86_64-linux-gnu/g"\
> /usr/local/epics_oag/epics/extensions/configure/os/CONFIG_SITE.linux-x86_64.linux-x86_642 \
  && mv /usr/local/epics_oag/epics/extensions/configure/os/CONFIG_SITE.linux-x86_64.linux-x86_64{2,}  || return


# agora, "compile" as configuracoes para instalacao das extensoes:
cd epics/extensions/configure/ && make  || return


# Agora, vamos corrigir um aparente bug de um dos Makefiles do SDDS.
# Abra o arquivo
#gedit /usr/local/epics_oag/epics/extensions/src/SDDS/SDDSaps/Makefile.OAG
# e adicione as seguintes linhas abaixo de "sddsgenericfit_SYS_LIBS += $(SYS_GSLLIB)"
#sdds2mpl_SYS_LIBS += $(SYS_GSLLIB)
#sddsmxref_SYS_LIBS += $(SYS_GSLLIB)
#sddsxref_SYS_LIBS += $(SYS_GSLLIB)
# isso eh necessario porque estamos usando a gsl do sistema. O makefile so usa a gsl
# para os codigos que realmente precisam dela, mas eles esqueceram desses tres ai...

sed '/sddsgenericfit_SYS_LIBS/{s/.*/&\nsdds2mpl_SYS_LIBS += \$(SYS_GSLLIB)\nsddsmxref_SYS_LIBS += \$(SYS_GSLLIB)\nsddsxref_SYS_LIBS += \$(SYS_GSLLIB)/;:a;n;ba}' \
/usr/local/epics_oag/epics/extensions/src/SDDS/SDDSaps/Makefile.OAG > /usr/local/epics_oag/epics/extensions/src/SDDS/SDDSaps/Makefile.OAG2 && \
mv /usr/local/epics_oag/epics/extensions/src/SDDS/SDDSaps/Makefile.OAG{2,} || return

# Agora, compile o SDDS e outras extensoes:
cd ../src/SDDS && make && cd ../oagca && make && cd ../SDDSepics && make  || return
cd /usr/local/epics_oag/epics/extensions/src/SDDS/python/ && make

# va para
#cd /usr/local/epics_oag/oag/apps/configure  || return
# e edite
#gedit RELEASE
# setando a variavel 
#EPICS_BASE=/usr/local/epics_oag/epics/base
echo ' ' >> /usr/local/epics_oag/oag/apps/configure/RELEASE || return
echo 'EPICS_BASE=/usr/local/epics_oag/epics/base' >> /usr/local/epics_oag/oag/apps/configure/RELEASE || return

# edite o comeco do arquivo
#gedit /usr/local/epics_oag/oag/apps/configure/CONFIG
# setando as variaveis:
#CROSS_COMPILER_TARGET_ARCHS =
#SHARED_LIBRARIES=YES
var='CROSS_COMPILER_TARGET_ARCHS='
cat /usr/local/epics_oag/oag/apps/configure/CONFIG | sed -e "s/$var.*/$var/g" \
> /usr/local/epics_oag/oag/apps/configure/CONFIG2 && mv /usr/local/epics_oag/oag/apps/configure/CONFIG{2,}  || return
var='SHARED_LIBRARIES='
cat /usr/local/epics_oag/oag/apps/configure/CONFIG | sed -e "s/${var}.*/${var}YES/g" \
> /usr/local/epics_oag/oag/apps/configure/CONFIG2 && mv /usr/local/epics_oag/oag/apps/configure/CONFIG{2,}  || return

# por fim, digite 
make

# Agora vamos compilar o Elegant e suas ferramentas:
cd /usr/local/epics_oag/oag/apps/src/physics && make && \
cd /usr/local/epics_oag/oag/apps/src/elegant && make  || return
# quando compilei o elegant na workstation nao tive problemas aqui
# mas quando compilei no meu computador, tive problemas com a definicao
# multipla da funcao xerbla nas bibliotecas lapack e blas.
# tente dar o make, caso vc tenha o mesmo problema entre na pasta
#cd O.linux-x86_64/
# copie o comando /usr/bin/g++ -o elegant -Wl,-Bstatic ...
# adicione a diretiva 
#/usr/bin/g++ -o elegant -Wl,--allow-multiple-definition -Wl,-Bstatic ...
# e faca a linkagem novamente


# para compilar o elegantTools entre na pasta
#cd elegantTools
# abra o arquivo
#gedit Makefile.OAG
# edite a variavel
#STATIC_BUILD=YES
# nessa versao ela esta na linha 174
var='STATIC_BUILD='
cat /usr/local/epics_oag/oag/apps/src/elegant/elegantTools/Makefile.OAG | sed -e "s/${var}.*/${var}YES/g" \
> /usr/local/epics_oag/oag/apps/src/elegant/elegantTools/Makefile.OAG2 && \
mv /usr/local/epics_oag/oag/apps/src/elegant/elegantTools/Makefile.OAG{2,}  || return

# E agora podemos compilar
make

# vamos compilar o xraylib e o sddsbrightness
cd ../xraylib && make && cd ../elegant/sddsbrightness && make &&\
cd /usr/local/epics_oag/oag/apps/src/tcltklib && make && \
cd /usr/local/epics_oag/oag/apps/src/tcltkapp/oagapp && make  || return


#Tive um problema aqui. O gcc não conseguia encontrar o header tcl.h
#Faça o seguinte:
#abra todos os Makefile.OAG das pastas que estão abaixo de extensions:
#gedit */*.OAG 
# e adicione isso no início do arquivo:
#TCL_INC = /usr/include/tcl8.6
#TK_INC = /usr/include/tk
#TK_LIB = /usr/lib/tcl8.6
#TCL_LIB = /usr/lib/tk8.6
Folder='ca'
sed '/SHARED_LIBRARIES/{s/.*/&\n\nTCL_INC = \/usr\/include\/tcl8.6\nTK_INC = \/usr\/include\/tk\nTK_LIB = \/usr\/lib\/tcl8.6\nTCL_LIB = \/usr\/lib\/tk8.6/;:a;n;ba}' \
$Folder/Makefile.OAG > $Folder/Makefile.OAG2 && mv $Folder/Makefile.OAG{2,} || return
Folder='os'
sed '/SHARED_LIBRARIES/{s/.*/&\n\nTCL_INC = \/usr\/include\/tcl8.6\nTK_INC = \/usr\/include\/tk\nTK_LIB = \/usr\/lib\/tcl8.6\nTCL_LIB = \/usr\/lib\/tk8.6/;:a;n;ba}' \
$Folder/Makefile.OAG > $Folder/Makefile.OAG2 && mv $Folder/Makefile.OAG{2,} || return
Folder='sdds'
sed '/SHARED_LIBRARIES/{s/.*/&\n\nTCL_INC = \/usr\/include\/tcl8.6\nTK_INC = \/usr\/include\/tk\nTK_LIB = \/usr\/lib\/tcl8.6\nTCL_LIB = \/usr\/lib\/tk8.6/;:a;n;ba}' \
$Folder/Makefile.OAG > $Folder/Makefile.OAG2 && mv $Folder/Makefile.OAG{2,} || return
Folder='rpn'
sed '/SHARED_LIBRARIES/{s/.*/&\n\nTCL_INC = \/usr\/include\/tcl8.6\nTK_INC = \/usr\/include\/tk\nTK_LIB = \/usr\/lib\/tcl8.6\nTCL_LIB = \/usr\/lib\/tk8.6/;:a;n;ba}' \
$Folder/Makefile.OAG > $Folder/Makefile.OAG2 && mv $Folder/Makefile.OAG{2,} || return
# Por fim, vá para 
cd /usr/local/epics_oag/oag/apps/src/tcltkinterp/extensions && make  || return

# por fim, de o comando 
./installExtensions -location /usr/local/epics_oag/oag/apps/lib/linux-x86_64/ || return


# Vamos criar links para o tclsh e o wish em: 
cd /usr/local/epics_oag/oag/apps/bin/linux-x86_64/ && \
ln -s /usr/bin/tclsh oagtclsh && ln -s /usr/bin/wish oagwish || return

####################
# Agora vamos compilar o Pelegant!
# agora é só compilar as bibliotecas do SDDS e o elegant:
cd /usr/local/epics_oag/epics/extensions/src/SDDS/SDDSlib && make clean && make MPI=1 && \
cd /usr/local/epics_oag/epics/extensions/src/SDDS/pgapack && make clean && make MPI=1 && \
cd /usr/local/epics_oag/oag/apps/src/elegant && make MPI=1 clean && make Pelegant

cd /usr/local/epics_oag/ && rm *.gz
