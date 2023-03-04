playing = true
$(document).ready(function(){
    const socket = io();
    //actions
    $('.left').click(function(){
        if (playing) socket.emit('next_pos', {'action':'left'})
    })
    $('.right').click(function(){
        if (playing) socket.emit('next_pos', {'action':'right'})
    })
    $('.up').click(function(){
        if (playing) socket.emit('next_pos', {'action':'up'})
    })
    $('.down').click(function(){
        if (playing) socket.emit('next_pos', {'action':'down'})
    })
    
    socket.on('update_status', (data)=>{
        curr = $(".curr_room")
        curr.removeClass("curr_room")

        room = $(".room[x='" + data['x'] + "'][y='" + data['y'] + "']")
        room.empty()
        if (data['pit'] == 2) {
            room.append("<i data-feather='x-circle'></i>")
        } else if (data['wumpus'] == 2) {
            room.append("<i data-feather='frown'></i>")
        } else if (data['treasure'] == 2) {
            room.append("<i data-feather='award'></i>")
        } else {
            if (data['pit'] == 1) {
                room.append("<i data-feather='wind'></i>")
            }
            if (data['wumpus'] == 1) {
                room.append("<i data-feather='alert-triangle'></i>")
            }
            if (data['treasure'] == 1) {
                room.append("<i data-feather='star'></i>")
            }
        }
        feather.replace()
        room.addClass("curr_room")
        room.addClass("vis_room")
    })
    
    // win or lose  
    socket.on('win', (data)=>{
        $('.win').css("display", "flex")
        $('.win').show("fast")
        playing = false
    })

    socket.on('lose', (data)=>{
        $('.lose').css("display", "flex")
        $('.lose').show("fast")
        playing = false
    })
    
// detecting arrow keys
$(document).keydown(function(e) {
    if (e.keyCode == 37) {
        //left
        if (playing) socket.emit('next_pos', {'action':'left'})
    } else if (e.keyCode == 38) {
        //up
        if (playing) socket.emit('next_pos', {'action':'up'})
    } else if (e.keyCode == 39) {
        //right
        if (playing) socket.emit('next_pos', {'action':'right'})
    } else if (e.keyCode == 40) {
        //down
        if (playing) socket.emit('next_pos', {'action':'down'})
    }
})

})
