function getType()
{
    var myselect = document.getElementById("type");
    return myselect.value;  
}
function changeType()
{   var c = document.getElementById("change");
    c.setAttribute("accept",getType());
}

function submit_query(btn){
    console.log(1);

    var sitv = setInterval(function(){
        var prog_url = '/index/p/';               // prog_url指请求进度的url，后面会在django中设置
        $.getJSON(prog_url, function(res){
            $('#prog_in').width(res + '%'); 
            console.log(res);    // 改变进度条进度，注意这里是内层的div， res是后台返回的进度
        });
    }, 50);                                 // 每1秒查询一次后台进度

    var this_url = 'index/loadData/';                      // 指当前页面的url
    var yourjson = 'beg';
    $.getJSON(thisurl, yourjson, function(res){
        
        clearInterval(sitv);                   // 此时请求成功返回结果了，结束对后台进度的查询
    });
}
