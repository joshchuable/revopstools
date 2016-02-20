var gulp = require('gulp'),
	uglify = require('gulp-uglify'),
	sass = require('gulp-ruby-sass'),
	postcss = require('gulp-postcss'),
	csswring = require('csswring'),
	autoprefixer = require('autoprefixer-core');

gulp.task('default', ['scripts', 'watch']);

// Scripts Task
// Uglifies JS
gulp.task('scripts', function(){
	// Source files
	gulp.src('static/src/js/*.js')
	.pipe(uglify())
	// Output folder
	.pipe(gulp.dest('static/build/js/'));
});

// Watch Task
// Watches JS
gulp.task('watch', function(){
	// Watch files location, then run the follow scripts
	gulp.watch('static/src/js/*.js', ['scripts']);
	gulp.watch('static/src/scss/**/*.scss', ['styles', 'css']);
});

// Styles Task
// Compiles CSS/Sass
gulp.task('styles', function(){
	// Source
	return sass('static/src/scss/scss.scss')
	// Destination
	.pipe(gulp.dest('static/src/css_debug/css_debug.css'));
});

// Post CSS
gulp.task('css', function () {

	var processors = [
		csswring({
			preserveHacks: true
		}),
		autoprefixer({
			browsers:['last 3 version']
		})
	];

    return sass('static/src/css_debug/css_debug.css', {
		style: 'compressed',
	})
        .pipe( postcss(processors) )
        .pipe( gulp.dest('static/build/css/style.css') );
});

