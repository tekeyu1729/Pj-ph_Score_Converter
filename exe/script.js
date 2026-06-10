let data = [];

fetch("data.json")
    .then(response => response.json())
    .then(json => {
        data = json;
        diff_setup();
        level_setup();
        music_setup();
    });

const setting = document.getElementById("setting");
const tuika = document.getElementById("tuika");

function openSettings(){setting.style.display = "flex";};
function closeSettings(){setting.style.display = "none";};

function opentuika(){tuika.style.display = "flex";};
function closetuika(){tuika.style.display = "none";};

let diff_0 = []
let level_0 = []
let music_0 = []
let combo_0 = []

const result = [];

function diff_setup(){
    for(let i=0;i<3;i++){
        const diff_1 = data[i].map(x => x[0]);
        diff_0.push(diff_1[0])
    }
    const diff_li = document.getElementById("diff");

    diff_0.forEach(i => {
        diff_li.add(new Option(i, i));
    });
}

function level_setup(){
    let diff_le=diff.selectedIndex
    for (let i=0;i<3;i++){
        if (diff_le==i){
            const level_0 = data[diff_le].map(x => x[0]);
            level_0.splice(0, 1);
            const level_li = document.getElementById("level");
            level_0.forEach(i => {
                level_li.add(new Option(i, i));
            });
        }
    }
}

function music_setup(){
    let diff_mu=diff.selectedIndex
    let level_mu=level.selectedIndex
    for(let k=0;k<3;k++){
        if (diff_mu==k){
            for(let i=0;i<(data[k].length-1);i++){
                if(level_mu==i){
                    const music_0 = data[k][i+1][1].map(x => x[0]);
                    const music_mu = document.getElementById("music");
                    music_0.forEach(i => {
                        music_mu.add(new Option(i, i));
                    });
                }
            }
        }
    }
}

const diff = document.getElementById("diff");
diff.addEventListener("change", () => {
    level.options.length = 0;
    level_setup();
    music.options.length = 0;
    music_setup();
});

const level = document.getElementById("level");
level.addEventListener("change", () => {
    music.options.length = 0;
    music_setup();
});

const diff_1 = document.getElementById("diff");
diff_0.forEach(di => {diff_1.add(new Option(di, di));});

const level_1 = document.getElementById("level");
level_0.forEach(le => {level_1.add(new Option(le, le));});

const music_1 = document.getElementById("music");
music_0.forEach(mu => {music_1.add(new Option(mu, mu));});

function calc_ca(){
let fu=data[diff.selectedIndex][level.selectedIndex+1][1][music.selectedIndex][1]
let ma=Number(ma_h.value)||0
let pa=Number(pa_h.value)||0
let gr=Number(gr_h.value)||0

score=(5/fu)*(9*(pa+gr*0.65)+ma)
if (score>=100) {
    score=100
    hantei=0
}else if (score>=96) {
    hantei=1
}else if (score>=92) {
    hantei=2
}else if (score>=88) {
    hantei=3
}else if (score>=82) {
    hantei=4
}else if (score>=70) {
    hantei=5        
}else{
    hantei=6
}

score=Math.round(10000*score);
let hantei_0=["φ","V","S","A","B","C","F"]
const result = document.getElementById("result");
result.textContent=`スコア: ${score} (${hantei_0[hantei]})`;
}
