#!/bin/sh

tag=$1

# Cleanup
rm -rf .build

# Build
swift build -c release

mkdir -p .build/output

# Zip
zip .build/output/very.zip .build/release/very

cd .build/output

# SHA256

shasum=`shasum -a 256 very.zip | cut -f1 -d' '`

gh release delete "$tag"
gh release create "$tag"
gh release upload "$tag" very.zip

git clone git@github.com:divadretlaw/homebrew-tap.git
cd homebrew-tap

sed "s/{{SHASUM}}/$shasum/" Templates/very.rb | sed "s/{{TAG}}/$tag/" > Formula/very.rb

git add Formula/very.rb
git commit -m "Update very"
git push

cd ..
rm -rf homebrew-tap