module.exports = function(grunt) {

  grunt.initConfig({
    pkg : grunt.file.readJSON('package.json'),
    jshint : {
      options: {
        node: true,
        esnext: true
      },
      files : [
        '*.js',
        'state_handlers/*.js'
      ]
    },
    jsdoc : {
      doc : {
        src : [
          '*.js',
          'state_handlers/*.js',
          '../README.md'
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
