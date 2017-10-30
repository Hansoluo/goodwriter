$(document).ready(function(){
$("#search").click(function() {
  key = $("#key").val();
  if (key != "") {
    $.post("get_material",{key:key,tag:""}, function(result) {
      if(result==""){
        $("#result").html("没有找到指定的值");
      }else {
        $("#result").html(result);
      }
    });
  } else {
    alert("关键词不能为空！");
  };
});
$("#search_tag").children('a').click(function() {
  tag = $(this).attr("title");
  if (tag != "") {
    $.post("get_material",{key:"",tag:tag}, function(result) {
      if(result==""){
        $("#result").html("没有找到指定的值");
      }else {
        $("#result").html(result);
      }
    });
  };
});
})
