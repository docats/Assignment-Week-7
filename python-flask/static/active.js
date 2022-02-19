function search(){
    let qname=document.getElementById('site_search').value;
    let rname=document.getElementById('rname')
    fetch('http://127.0.0.1:3000/api/members?username='+qname,
    ).then((response) =>{
        // console.log("response.json():",response.json()); //撈出json資料
        return response.json();
    }).then((json)=>{
        console.log("json:",json);
         if(json.data==null){  //如果json沒有資料
            console.log("json.data:",json.data)
            return rname.innerHTML = "沒有資料"
        }
        else{ //如果有資料
            let name=json.data.name;
            let username=json.data.username;
            console.log("name:",name);
            // rname.innerHTML=name+ "("+rname+")"
            rname.innerHTML=name+ "("+qname+")";   
        }
    }).catch((error)=>{
        return error
    })
}

