// ==UserScript==
// @name         ArchWiki Copy Revision Number
// @namespace    https://github.com/dybdeskarphet/archwiki-tools
// @version      0.0.1
// @description  FAB to copy the revision number in ArchWiki
// @author       Ahmet Arda Kavakcı
// @match        *://wiki.archlinux.org/*
// @grant        GM_addStyle
// ==/UserScript==

(function () {
  "use strict";

  function extractRevisionNumber() {
    const scripts = document.querySelectorAll("script");
    for (const script of scripts) {
      const match = script.textContent.match(/"wgCurRevisionId":(\d+)/);
      if (match) {
        return match[1];
      }
    }
    return null;
  }

  function showToast(message) {
    const toast = document.createElement("div");
    toast.className = "custom-toast";
    toast.textContent = message;

    document.body.appendChild(toast);
    setTimeout(() => {
      toast.classList.add("show");
    }, 100);

    setTimeout(() => {
      toast.classList.remove("show");
    }, 3000);
  }

  function addCopyRevisionButton() {
    const revisionNumber = extractRevisionNumber();
    if (!revisionNumber) {
      console.error("Revision number not found");
      return;
    }
    console.log("Revision number found:", revisionNumber);

    var copyButton = document.createElement("button");
    copyButton.innerHTML = "📋 Copy Revision Number";
    copyButton.className = "fab-copy-revision";

    copyButton.addEventListener("click", function () {
      navigator.clipboard.writeText(revisionNumber).then(
        function () {
          showToast("Revision number copied to clipboard");
        },
        function (err) {
          showToast("Failed to copy revision number");
          console.error("Could not copy revision number:", err);
        }
      );
    });

    document.body.appendChild(copyButton);
  }

  GM_addStyle(`
        .fab-copy-revision {
            position: fixed;
            bottom: 20px;
            right: 20px;
            min-width: 200px;
            height: 56px;
            border-radius: 28px;
            background-color: #333333;
            color: white;
            border: none;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            font-size: 16px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            padding: 0 15px;
        }

        .custom-toast {
            visibility: hidden;
            min-width: 250px;
            margin-left: -125px;
            background-color: black;
            color: white;
            text-align: center;
            border-radius: 2px;
            padding: 16px;
            position: fixed;
            z-index: 1001;
            left: 50%;
            bottom: 30px;
            font-size: 17px;
            border-radius: 20px
        }

        .custom-toast.show {
            visibility: visible;
            -webkit-animation: fadein 0.5s, fadeout 0.5s 2.5s;
            animation: fadein 0.5s, fadeout 0.5s 2.5s;
        }

        @-webkit-keyframes fadein {
            from {bottom: 0; opacity: 0;}
            to {bottom: 30px; opacity: 1;}
        }

        @keyframes fadein {
            from {bottom: 0; opacity: 0;}
            to {bottom: 30px; opacity: 1;}
        }

        @-webkit-keyframes fadeout {
            from {bottom: 30px; opacity: 1;}
            to {bottom: 0; opacity: 0;}
        }

        @keyframes fadeout {
            from {bottom: 30px; opacity: 1;}
            to {bottom: 0; opacity: 0;}
        }
    `);

  window.addEventListener("load", addCopyRevisionButton);
})();
