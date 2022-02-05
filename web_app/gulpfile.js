const fs = require('fs');
const gulp = require('gulp');
const inlinesource = require('gulp-inline-source');
const replace = require('gulp-replace');

gulp.task('default', () => {
  const file = fs.readFileSync('./build/index.html', {
    encoding: 'utf8',
    flag: 'r',
  });
  const regex = /<script defer="defer" src=".+?"><\/script>/;
  const scriptTags = file.match(regex);
  let html = file;
  console.log(scriptTags);

  scriptTags.forEach((tag) => {
    html = html.replace(tag, '');
    html = html.replace(
      '<div id="root"></div>',
      `<div id="root"></div>
       ${scriptTags.join('')}`,
    );
  });
  fs.writeFileSync('./build/index.html', html);
  return gulp
    .src('./build/index.html')
    .pipe(replace('.js"></script>', '.js" inline></script>'))
    .pipe(replace('rel="stylesheet">', 'rel="stylesheet" inline>'))
    .pipe(
      inlinesource({
        compress: false,
        ignore: ['png'],
      }),
    )
    .pipe(gulp.dest('./dist/'));
});
