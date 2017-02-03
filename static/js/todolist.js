Vue.component('todo', {
  props: ['task'],
  template: '<li>{{ task }}</li>'
});

var vm = new Vue({
  el: '#todo-list',
  data: {
    todoList: null,
    newTodo: null
  }
});

$.ajax({
  url: '/todos'
}).done(function(data) {
  vm.$data.todoList = data;
});

$('#add-todo').submit(function(e) {
  e.preventDefault();
  $.ajax({
    url: '/todos',
    method: 'POST',
    data: vm.newTodo
  }).done(function(data) {
    console.log(data);
  });
});

