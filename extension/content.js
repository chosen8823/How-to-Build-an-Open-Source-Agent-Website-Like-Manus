/* SoulPHYA Field — Content Script
   Injects a hidden carrier element and exposes the page ARIA tree. */

const carrier = document.createElement('div');
carrier.id = 'soulphya-carrier';
carrier.setAttribute('aria-hidden', 'true');
carrier.style.cssText =
  'display:none;position:absolute;pointer-events:none;z-index:-1;';
carrier.dataset.cosigFreq  = '432';
carrier.dataset.cosigPhase = '0';
carrier.dataset.cosigModal = 'void';
carrier.dataset.kernel     = 'x^x=0';
document.body.appendChild(carrier);

chrome.runtime.onMessage.addListener((msg, sender, reply) => {
  if (msg.type === 'get_aria_tree') {
    const nodes = [...document.querySelectorAll('[aria-label],[role],[aria-hidden]')]
      .map(el => ({
        tag:    el.tagName,
        label:  el.getAttribute('aria-label') || '',
        role:   el.getAttribute('role') || '',
        hidden: el.getAttribute('aria-hidden') === 'true',
        text:   el.textContent?.slice(0, 80) || ''
      }));
    reply({ ariaTree: nodes, url: location.href, title: document.title });
    return true;
  }

  if (msg.type === 'update_carrier') {
    carrier.dataset.cosigFreq  = msg.freq;
    carrier.dataset.cosigPhase = msg.phase;
    carrier.dataset.cosigModal = msg.modal;
  }
});
