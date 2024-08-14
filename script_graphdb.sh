#!/bin/sh
sed -i 's~t.otherwise({templateUrl:"pages/not_found.html"}),~t.when("/vocabulary/:id*", { redirectTo: (routeParams) => `/resource?uri=http://kflow.eurecom.fr/vocabulary/${routeParams.id}`}),t.otherwise({templateUrl:"pages/not_found.html"}),~g' /opt/graphdb/dist/lib/workbench/bundle.232a4218c3d298e1979f.bundle.js


#!/bin/sh
sed -i 's~t.otherwise({templateUrl:"pages/not_found.html"}),~t.when("/condition/:id*", { redirectTo: (routeParams) => `/resource?uri=http://kflow.eurecom.fr/condition/${routeParams.id}`}),t.otherwise({templateUrl:"pages/not_found.html"}),~g' /opt/graphdb/dist/lib/workbench/bundle.232a4218c3d298e1979f.bundle.js


#!/bin/sh
sed -i 's~t.otherwise({templateUrl:"pages/not_found.html"}),~t.when("/paper/:id*", { redirectTo: (routeParams) => `/resource?uri=http://kflow.eurecom.fr/paper/${routeParams.id}`}),t.otherwise({templateUrl:"pages/not_found.html"}),~g' /opt/graphdb/dist/lib/workbench/bundle.232a4218c3d298e1979f.bundle.js


#!/bin/sh
sed -i 's~t.otherwise({templateUrl:"pages/not_found.html"}),~t.when("/provenance/:id*", { redirectTo: (routeParams) => `/resource?uri=http://kflow.eurecom.fr/provenance/${routeParams.id}`}),t.otherwise({templateUrl:"pages/not_found.html"}),~g' /opt/graphdb/dist/lib/workbench/bundle.232a4218c3d298e1979f.bundle.js


#!/bin/sh
sed -i 's~t.otherwise({templateUrl:"pages/not_found.html"}),~t.when("/event/:id*", { redirectTo: (routeParams) => `/resource?uri=http://kflow.eurecom.fr/event/${routeParams.id}`}),t.otherwise({templateUrl:"pages/not_found.html"}),~g' /opt/graphdb/dist/lib/workbench/bundle.232a4218c3d298e1979f.bundle.js
