# marketplace_api

## TODOs

#### apps

- [x] base users endpoints: `CRUD` and `set_password`
- [x] base authorization endpoints with JWT tokens
- [x] base sellers endpoints
- [ ] products
  - [ ] reviews
- [ ] cart
- [ ] buyer orders/seller orders
- [ ] payments

#### steps and logic

- [ ] users
  - [x] models
  - [x] CRUD for users
  - [ ] CRUD tests
  - [ ] `set_email`, `set_email_confirm` endpoints and validate email in user creation
- [ ] sellers
  - [x] models
  - [x] CRUD for sellers
  - [ ] CRUD tests
- [ ] auth
  - [x] jwt
  - [ ] login endpoint
  - [ ] OTP
  - [ ] oauth2
- [ ] products
  - [ ] models(products, categories, reviews + review and products images: продумать как они будут сохраняться и получаться)
  - [ ] CRUD for products
  - [ ] Products searching, filtering, ordering. Searching by category
  - [ ] Favorites products(избранное, понравившееся, сердечко типа)
- [ ] cart
  - [ ] models
  - [ ] возможность добавлять товары в корзину
  - [ ] удалять товары из корзины
  - [ ] чистить корзину полностью
  - [ ] корзина одна на одного юзера
- [ ] byuer and seller orders
  - [ ] список заказов покупателя + список заказов, которые видны у продавцов: кто заказал, адрес доставки, список товаров
- [ ] payments
- [ ] adresses - для доставок
