import Mercury from '@postlight/mercury-parser';
import process from 'process';
import iconv from 'iconv-lite';
import fs from 'fs';

iconv.skipDecodeWarning = true;

const url = process.argv[2];
const options = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));

Mercury.parse(url, options).then(result => console.log(JSON.stringify(result)));