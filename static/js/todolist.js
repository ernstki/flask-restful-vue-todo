/*********************************************************************//**
 *                                                                       *
 *   Vue.js to-do list application                                       *
 *                                                                       *
 *   Author: Kevin Ernst <ernstki -at- mail.uc.edu>                      *
 *   Home:   https://github.uc.edu/flask-restful-todo                    *
 *                                                                       *
/*************************************************************************/
'use strict';

var todoAPI = {
  'fetch': function(id) {
  },

  'fetchAll': function() {
  },

  'update': function(id, task) {
  },

  'delete': function(id, task) {
  }
};

//Vue.component('todo', {
// props: ['task'],
// template: '<li>{{ task }}</li>'
//});

var msg = new Vue({
  el: '#status-msg',
  data: {
    message: null,
    lasterror: null,
    status: 200
  }
});

var vm = new Vue({
  el: '#todo-container',

  data: {
    api: fetchival('/todos'),
    todo: { task: '', done: false },
    todos: [],
    //nextid: 0
  },

  mounted: function() {
    this.fetchToDos();
    document.getElementById('loading-msg').style.display = 'none';
    document.getElementById('todo-list').style.display = 'inline';
  },

  methods: {
    fetchToDos: function() {
      this.api
        .get()
        .then(function(json) {
          // can I use 'this' here? sigh, JavaScript.
          vm.$set(vm.$data, 'todos', json);
        })
        .catch(function(err) {
          // Fall back to some hard-coded local defaults
          var todos = [
            { id: 1, task: 'water the cactus', done: false },
            { id: 2, task: 'heal the world', done: false }
          ];
          vm.$set(vm.$data, 'todos', todos);

          // FIXME: update an error message somewheres in the UI
          throw new Error('Fetching todos failed (status: '
                          + err.response.status + ' ' + err.response.statusText
                          + ')');
        });
    },

    addToDo: function() {
      // FIXME: Duplicated code with 'fetchToDos' above
      if (this.todo.task) {
        var addIt = function(json) {
          vm.$data.todos.push(json);
          vm.$data.todo = { task: '', done: false };
          console.log('Added to-do ID ' + json.id);
        };

        this.api
          .put(this.todo)
          .then(addIt)
          .catch(function(err) {
            // FIXME: update an error message somewheres in the UI
            throw new Error("Adding todo '" + json.task +"' failed (status: " +
                            err.response.status + ')');
          });
      } // if the task isn't empty
    },

    toggleDone: function(id) {
      var key; // keep track of the one that matches 'id'

      _.map(this.todos, function(e,k) {
        if (e.id === id) {
          key = k;
        }
        return e;
      });

      var todo = this.todos[key];  // get a reference to it

      var toggleIt = function(json) {
          todo.done = todo.done ? false : true;  // toggle its value
          console.log('Marked to-do ID ' + id + ' as ' +
                      (todo.done ? 'done.' : 'not done.'));
      };

      this.api(id)
        .put(todo)
        .then(toggleIt)
        .catch(function(err) {
          // FIXME: update an error message somewheres in the UI
          throw new Error('Toggling to-do ID ' + todo.id + ' failed (status: '
                          + err.response.status + ' ' + err.response.statusText
                          + ')');
        });
    }, // toggleDone

    deleteToDo: function(id) {
      // It seems like it's necessary to wrap this in a function so that it
      // closes around the value of 'id' in this function's scope.
      var deleteIt = function() {
        vm.$data.todos = _.reject(vm.$data.todos, function(e) {
          return e.id === id;
        });
        console.log('Deleted to-do ID ' + id);
      };

      this.api(id)
        .delete()
        .then(deleteIt)
        .catch(function(err) {
          // FIXME: update an error message somewheres in the UI
          throw new Error('DELETE of ID ' + id + ' failed (status: '
                          + err.response.status + ' ' + err.response.statusText
                          + ')');
        });
    } // deleteToDo
  } // methods
});
