/**
 * This is the client-side library that powers the "Flow" architecture.
 * It's a single, global function that handles intercepting form submits,
 * calling the backend, and swapping the HTML response into the DOM.
 */
async function flow(action, params, triggerElement) {
    console.log(`Flow triggered: ${action}`, params);

    // Convention: Action string 'products.add_item' is split into the
    // flow name ("products") and the method name ("add_item").
    const [flowName, methodName] = action.split('.');

    try {
        const response = await fetch('/___flow___', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                flow: flowName,
                method: methodName,
                params: params
            }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Flow Error:', response.status, errorText);
            alert(`Server error: ${errorText}`);
            return;
        }

        const html = await response.text();

        // Find the declarative attributes on the element that triggered the flow
        // (e.g., the <form> element).
        const targetSelector = triggerElement.getAttribute('flow:target');
        const swapMethod = triggerElement.getAttribute('flow:swap') || 'innerHTML'; // Default to innerHTML

        if (!targetSelector) {
            console.error('Flow Error: No "flow:target" attribute found on the trigger element.', triggerElement);
            return;
        }

        const targetElement = document.querySelector(targetSelector);
        if (!targetElement) {
            console.error(`Flow Error: Target element "${targetSelector}" not found.`);
            return;
        }

        console.log(`Swapping content into ${targetSelector} using ${swapMethod}`);

        // Perform the DOM update based on the swap method.
        switch (swapMethod) {
            case 'innerHTML':
                targetElement.innerHTML = html;
                break;
            case 'outerHTML':
                targetElement.outerHTML = html;
                break;
            case 'beforeend':
                targetElement.insertAdjacentHTML('beforeend', html);
                break;
            case 'afterbegin':
                targetElement.insertAdjacentHTML('afterbegin', html);
                break;
            case 'beforebegin':
                targetElement.insertAdjacentHTML('beforebegin', html);
                break;
            case 'afterend':
                targetElement.insertAdjacentHTML('afterend', html);
                break;
            default:
                console.error(`Flow Error: Unknown swap method "${swapMethod}"`);
        }
    } catch (error) {
        console.error('Flow network or JS error:', error);
        alert('A network error occurred. Please check the console.');
    }
}
