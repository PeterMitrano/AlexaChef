module.exports = function(grunt) {

  grunt.initConfig({
    pkg : grunt.file.readJSON('package.json'),
    jshint : {
      files : [
        'Gruntfile.js',
        'src/index.js'
      ]
    },
    jsdoc : {
      doc : {
        src : [
          'src/AlexaSkill.js',
          'src/index.js',
        ],
        options : {
          destination : 'doc'
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
