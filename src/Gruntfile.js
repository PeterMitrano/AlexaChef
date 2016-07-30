module.exports = function(grunt) {

  grunt.initConfig({
    pkg : grunt.file.readJSON('package.json'),
    jshint : {
      options: {
        node: true,
        esnext: true
      },
      files : [
        '*.js'
      ]
    },
    jsdoc : {
      doc : {
        src : [
          '*.js',
        ],
        options : {
          destination : '../doc'
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-jsdoc');

  grunt.registerTask('dev', ['jshint']);
  grunt.registerTask('doc', ['jsdoc']);
  grunt.registerTask('default', ['dev', 'doc']);
};
