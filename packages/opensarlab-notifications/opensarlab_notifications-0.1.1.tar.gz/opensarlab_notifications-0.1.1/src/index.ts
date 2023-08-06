import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

import jQuery from 'jquery';
import toastr from 'toastr';

const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-topbar-opensarlab-notifications',
  autoStart: true,
  activate: async (app: JupyterFrontEnd) => {
    try {
        let toastrLink = document.createElement('link')
        toastrLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css'
        toastrLink.rel = 'stylesheet'
        document.head.appendChild(toastrLink)

        jQuery( document ).ready(function() {
            toastr.options = {
                "closeButton": true,
                "newestOnTop": true,
                "progressBar": true,
                "positionClass": "toast-top-right",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": 30,
                "hideDuration": 1,
                "timeOut": 0,
                "extendedTimeOut": 0,
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            };

            fetch('opensarlab-notifications/notifications' )
                .then( response => response.json() )
                .then( notes => {
                    console.log(notes)
                    notes['data'].forEach( function (entry: any) {
                        (toastr as any)[entry.type](entry.message, entry.title)
                        }
                    )
                })
                .catch( error => console.log(error) )
        });
    } catch (reason) {
        console.error(`Error on GET opensarlab-notifications/notifications.\n${reason}`);
    }
  },
};

export default extension;
