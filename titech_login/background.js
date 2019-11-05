var username='';
password='';
matrix=[];

function get_user_info() {
  return {'username':username, 'password':password, 'matrix':matrix};
}

function save_user_info(new_student_id, new_password, new_matrix) {
  username = new_student_id;
  password = new_password
  matrix = new_matrix;
  var obj = {'username':new_student_id, 'password':new_password, 'matrix':new_matrix};
  obj = JSON.stringify(obj);
  localStorage.setItem("titch_login_date", obj);
}
function load_user_info() {
  result = JSON.parse(localStorage.getItem("titch_login_date"));
  if (result != null) {
    username = result.username;
    password = result.password;
    matrix = result.matrix;
  } else {

  }
}
document.addEventListener('DOMContentLoaded', function () {
  load_user_info();
});
