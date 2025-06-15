const primaryNav = document.getElementById("nav");
const secondNav = document.querySelector(".navSecond");
const overlayNavItem = document.getElementById("overlay_nav_item");

function openNavTop() {
        document.getElementById("myNavTop").style.width = "100%";
      }

function closeNavTop() {
        document.getElementById("myNavTop").style.width = "0%";
    }

const windowResizeCheck = function () {
        if (window.innerWidth < 1000) {
                //Remove the side bar
                primaryNav.style.display = "none";
                secondNav.style.display = "flex";
                secondNav.style.justifyContent = "space-between";
            } else {
                  primaryNav.style.display = "flex";
                  secondNav.style.display = "none";
                }
            }
windowResizeCheck();

window.addEventListener("resize", windowResizeCheck);
overlayNavItem.addEventListener("click", openNavTop);

