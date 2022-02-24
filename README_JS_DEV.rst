In package.json config:
 - vue.css.extract.chunkFilename
 - vue.css.extract.filename
 - vue.configureWebpack.output.filename
 - vue.configureWebpack.output.chunkFilename
 [hash:8] is used due to better browser cache handling. chunkFilename has [name] included to

 prevent same file names.