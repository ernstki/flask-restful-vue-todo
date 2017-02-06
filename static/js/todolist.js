//var todoAPI = {
//  fetch: function() {
//    $.ajax({
//      url: '/todos'
//    }).done(function(data) {
//      vm.$data.todoList = data;
//    });

//Vue.component('todo', {
// props: ['task'],
// template: '<li>{{ task }}</li>'
//});

var vm = new Vue({
  el: '#todo-container',

  data: {
    todo: { id: -1, task: '', done: false  },
    todos: [],
    nextid: 0
  },

  mounted: function() {
    this.fetchToDos();
    document.getElementById('loading-msg').style.display = 'none';
    document.getElementById('todo-list').style.display = 'inline';
  },

  methods: {
    fetchToDos: function() {
      var todos = [
        { id: 1, task: 'water the cactus', done: false },
        { id: 2, task: 'heal the world', done: false }
      ];
      this.todos = todos;

      // next id one higher than the biggest found in the list
      this.nextid = _.max(_.flatMap(this.todos, function(e) {
        return e.id })) + 1;
    },

    addToDo: function(e) {
      e.preventDefault();
      if (this.todo.task) {
        this.todo.id = this.nextid;
        this.todos.push(this.todo);
        console.log(this.todo.id);

        // set up for next time
        this.nextid = this.nextid + 1;
        this.todo = { id: this.nextid, task: '', done: false }
      }
    },

    toggleDone: function(index) {
      if (this.todos[index].done) {
        console.log('Marked to-do ID ' + index + ' as not done.');
        this.todos[index].done = false;
      } else {
        console.log('Marked to-do ID ' + index + ' as done.');
        this.todos[index].done = true;
      }
    }, 

    deleteToDo: function(index) {
      this.todos.splice(index, 1);
    }
  } // methods
});

//$('#add-todo').submit(function(e) {
//  e.preventDefault();
//  $.ajax({
//    url: '/todos',
//    method: 'POST',
//    data: vm.newTodo
//  }).done(function(data) {
//    console.log(data);
//  });
//});

