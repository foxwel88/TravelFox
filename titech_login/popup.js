// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

var flag = true;

function verify(){
  var user_info = chrome.extension.getBackgroundPage().get_user_info();
  if (user_info == null || check(user_info)) {
    chrome.tabs.executeScript(null,{code:"alert('please set your information!');"});
    return;
  }
  var matrix = user_info.matrix;

  chrome.tabs.getSelected(null, function (tab) {
    chrome.tabs.sendMessage(tab.id, {greeting: "hello"}, function(response) {
        chrome.tabs.executeScript(null,
          {code:"var blank1=document.querySelector('#authentication > tbody > tr:nth-child(5) > td > div > div > input');blank1.value='"+matrix[response[0]][response[1]]+"';" +
          "var blank2=document.querySelector('#authentication > tbody > tr:nth-child(6) > td > div > div > input');blank2.value='"+matrix[response[2]][response[3]]+"';" +
          "var blank3=document.querySelector('#authentication > tbody > tr:nth-child(7) > td > div > div > input');blank3.value='"+matrix[response[4]][response[5]]+"';" +
          "var button2=document.querySelector('#authentication > tbody > tr:nth-child(9) > td > input[type=submit]:nth-child(1)');button2.click();"
      });
    });
  });
}

function check(user_info) {
  if (user_info.username == null || user_info.username.length == 0 || user_info.password == null || user_info.password.length == 0 || user_info.matrix == null || user_info.matrix.length == 0) {
    return true;
  }
  return false;
}

function login() {
  var user_info = chrome.extension.getBackgroundPage().get_user_info();
  if (user_info == null || check(user_info)) {
    chrome.tabs.executeScript(null,{code:"alert('please set your information!');"});
    return;
  }
  var username = user_info.username;
  var password = user_info.password;
  chrome.tabs.executeScript(null,{code:"var inputs = document.querySelector('body > center:nth-child(5) > form > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > div > div > input');inputs.value='"+username+"';var inputs2=document.querySelector('body > center:nth-child(5) > form > table > tbody > tr > td > table > tbody > tr:nth-child(3) > td > div > div > input');inputs2.value='"+password+"';var button=document.querySelector('body > center:nth-child(5) > form > table > tbody > tr > td > table > tbody > tr:nth-child(5) > td > input[type=submit]:nth-child(1)');button.click();"}); 
}

function click(e) {
  if (e.target.id=='login') {
    login();
  }	
  if (e.target.id=='verify') {
    verify();
  }
  if (e.target.id=='setting') {
    document.getElementById('setting').style.display='none';
    document.getElementById('setting_pan').style.display='block';
    var user_info = chrome.extension.getBackgroundPage().get_user_info();
    document.getElementById('student_id').value=user_info.username;
    document.getElementById('password').value=user_info.password;
    var text = "";
    for (var i = 0; i < 7; i++) { 
      for (var j = 0; j < 10; j++) {
        text += user_info.matrix[j][i];
      }
      if (i<6) text += "\n";
    }
    document.getElementById('matrix').value=text;
  }
  if (e.target.id=='submit') {
    document.getElementById('setting').style.display='block';
    document.getElementById('setting_pan').style.display='none';
    var new_student_id = document.getElementById('student_id').value;
    var new_password = document.getElementById('password').value;
    var matrix_str = document.getElementById('matrix').value;
    var new_matrix = new Array();
    for (var i = 0; i < 10; ++i) {
      new_matrix[i] = new Array();
    }
    var ii = 0;
    var jj = 0;
    for (var i = 0; i < matrix_str.length; ++i) {
      if ((matrix_str[i] >= 'A' && matrix_str[i] <= 'Z') || (matrix_str[i] >= 'a' && matrix_str[i] <= 'z')) {
        new_matrix[ii][jj] = matrix_str[i].toUpperCase();
        ii++;
        if (ii >= 10) {
          ii = 0;
          jj++;
          if (jj >= 7) {
            break;
          }
        }
      }
    }
    chrome.extension.getBackgroundPage().save_user_info(new_student_id, new_password, new_matrix);
  }
}

chrome.tabs.onUpdated.addListener(
  function(tabId,changeInfo,tab){ 
    if (changeInfo.status == "complete")
    {
      if (tab.url=="https://portal.nap.gsic.titech.ac.jp/GetAccess/Login?Template=idg_key&AUTHMETHOD=IG&GASF=CERTIFICATE,IG.GRID,IG.OTP&LOCALE=ja_JP&GAREASONCODE=13&GAIDENTIFICATIONID=UserPassword&GARESOURCEID=resourcelistID2&GAURI=https://portal.nap.gsic.titech.ac.jp/GetAccess/ResourceList&Reason=13&APPID=resourcelistID2&URI=https://portal.nap.gsic.titech.ac.jp/GetAccess/ResourceList"){
        verify();
      }
    }
  });

document.addEventListener('DOMContentLoaded', function () {

  if (flag) {
    flag = false;
    document.getElementById('login').addEventListener('click', click);
    document.getElementById('verify').addEventListener('click', click);
    document.getElementById('setting').addEventListener('click', click);
    document.getElementById('submit').addEventListener('click', click);
  }
});
