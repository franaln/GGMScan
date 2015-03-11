ROOTDIR=$PWD

## get SUSYHIT package
echo
echo "*** getting SUSYHIT package from source..."
mkdir SUSYHIT
cd SUSYHIT
curl -O http://www.itp.kit.edu/~maggie/SUSY-HIT/susyhit.tar.gz

## untar
echo
echo ">> extracting..."
tar zxfv susyhit.tar.gz

## compile it
echo
echo ">> compiling..."
make

## configure
echo
echo ">> configuring..."
awk '/called/{print;getline;sub("1","2");print;next}1' susyhit.in > tmptmp.tmp
mv tmptmp.tmp susyhit.in
echo 'done!'

cd $ROOTDIR

## get SuSpect package
echo
echo "*** getting SuSpect package from source..."
mkdir -p SuSpect
cd SuSpect
curl -O http://www.coulomb.univ-montp2.fr/perso/jean-loic.kneur/Suspect/suspect2.tar.gz

## untar
echo
echo ">> extracting..."
tar zxfv suspect2.tar.gz

## compile it
echo
echo ">> compiling..."
echo 'g77 -c suspect2_call.f suspect2.f twoloophiggs.f bsg.f' > compileit.sh
echo 'g77 -o suspect2 suspect2_call.o suspect2.o twoloophiggs.o bsg.o' >> compileit.sh
chmod +x compileit.sh
. compileit.sh

cd $ROOTDIR

## create
echo
echo ">> creating dir structure..."
mkdir -p RunDir/plots
mkdir -p RunDir/logs
mkdir -p RunDir/output/SLHA

##create envsetup script
echo "export SGRIDENV=$PWD" > env.sh
chmod +x env.sh

echo
echo "GO!!"
echo
