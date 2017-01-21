mkdir tmp
cd tmp
git clone git://github.com/jquery/jquery.git
cd jquery
npm install grunt grunt-cli
npm install .
grunt custom:-ajax/jsonp,-ajax/parseXML,-deprecated,-dimensions,-event/focusin,-event/trigger,-offset,-wrap,-exports/amd
cp dist/jquery.min.js ../../js/custom-jquery.js
cd ../../
rm -rf tmp

