# Register Device App - Algotik 

this app provides an API to perform as an external API for a ecommerce website, below are the purpose of each endpoint and API goal: 

## endpoints
- ### Wordpress webhooks
    - create order replica: /api/order/create/
        - POST
        - data-type: application/json
        - data map: { "id": <id of the Wordpress order> , "" }