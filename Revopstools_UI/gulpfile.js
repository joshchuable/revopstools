var gulp = require('gulp'),
	uglify = require('gulp-uglify'),
	sass = require('gulp-ruby-sass'),
	concat = require('gulp-concat'),
	autoprefixer = require('gulp-autoprefixer');

gulp.task('default', ['scripts', 'styles', 'build_css', 'watch']);

// Scripts Task
// Uglifies JS
gulp.task('scripts', function(){
	// Source files
	gulp.src('static/src/js/*.js')
	.pipe(concat('scripts.js'))
	// .pipe(uglify())
	// Output folder
	.pipe(gulp.dest('static/build/js/'));
});

// Watch Task
// Watches JS
gulp.task('watch', function(){
	// Watch files location, then run the follow scripts
	gulp.watch('static/src/js/*.js', ['scripts']);
	gulp.watch('static/src/scss/**/*.scss', ['styles', 'build_css']);
});

// Styles Task
// Compiles CSS/Sass for Debugging
gulp.task('styles', function(){
	// Source
	return sass('static/src/scss/style.scss', {
		style: 'expanded'
	})
	.pipe(autoprefixer({
		browsers: ['last 3 versions'],
		cascade: false
	}))
	// Destination
	.pipe(gulp.dest('static/src/css_debug/'));
});

// Build CSS Task
// Compiles CSS/Sass
gulp.task('build_css', function(){
	// Source
	return sass('static/src/scss/style.scss', {
		style: 'compressed'
	})
	.pipe(autoprefixer({
		browsers: ['last 3 versions'],
		cascade: false
	}))
	// Destination
	.pipe(gulp.dest('static/build/css/'));
});

