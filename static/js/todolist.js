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
  el: '#todo-list',
  data: {
    todoList: { },
    newTodo: null
  }
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

