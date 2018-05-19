#!/bin/sh

cd ~/PKGBUILD
git pull
latestcommit=$(git rev-parse @)
prelatest=$(git rev-parse @~)
message=$(git log --format=%B -n 1 | head -n -1)
path=$(git diff $prelatest $latest --name-only)
pkgname=${path%%/*}
echo $path
cd ~/aur
git clone "ssh://aur@aur.archlinux.org/$pkgname"
rm $pkgname/*
cp -ar ~/PKGBUILD/$pkgname/* $pkgname/
cd $pkgname && git add *
git commit -m "$message"
git push
rm -rf ~/aur/$pkgname

