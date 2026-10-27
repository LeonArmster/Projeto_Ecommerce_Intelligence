# =====================================================
# Gerador de dados
# =====================================================
# Bibliotecas
from ecommerce_intelligence.config.config import raw_dir
from ecommerce_intelligence.generator.customer import generate_customers
from ecommerce_intelligence.generator.products import generate_products
from ecommerce_intelligence.generator.orders import generate_orders
from ecommerce_intelligence.generator.order_items import generate_order_items
from ecommerce_intelligence.generator.payments import generate_payments
from ecommerce_intelligence.generator.shipments import generate_shipments
from ecommerce_intelligence.generator.reviews import generate_reviews


# Função de orquestração de geração
def main() -> None:

    print("Gerando clientes...")

    customers = generate_customers(
        number_customers=100_000,
    )

    customers.to_parquet(
        raw_dir / "customers.parquet",
        index=False,
    )

    print(f"Clientes gerados: {len(customers):,}")

    print("Gerando produtos...")

    products = generate_products(
        number_products=20_000,
    )

    products.to_parquet(
        raw_dir / "products.parquet",
        index=False,
    )

    print(f"Produtos gerados: {len(products):,}")


    print("Gerando pedidos...")

    orders = generate_orders(
        customers=customers,
        number_orders=1_000_000,
    )

    orders.to_parquet(
        raw_dir / "orders.parquet",
        index=False,
    )

    print(f"Pedidos gerados: {len(orders):,}")


    print("Gerando itens dos pedidos...")

    order_items = generate_order_items(
        orders=orders,
        products=products,
    )

    order_items.to_parquet(
        raw_dir / "order_items.parquet",
        index=False,
    )

    print(
        f"Itens dos pedidos gerados: "
        f"{len(order_items):,}"
    )


    print("Gerando pagamentos...")

    payments = generate_payments(
        orders=orders,
        order_items=order_items,
    )

    payments.to_parquet(
        raw_dir / "payments.parquet",
        index=False,
    )

    print(f"Pagamentos gerados: {len(payments):,}")


    print("Gerando entregas...")

    shipments = generate_shipments(
        orders=orders,
        customers=customers,
    )

    shipments.to_parquet(
        raw_dir / "shipments.parquet",
        index=False,
    )

    print(f"Entregas geradas: {len(shipments):,}")


    print("Gerando avaliações...")

    reviews = generate_reviews(
        shipments=shipments,
    )

    reviews.to_parquet(
        raw_dir / "reviews.parquet",
        index=False,
    )

    print(f"Avaliações geradas: {len(reviews):,}")


    print("Geração concluída.")


if __name__ == "__main__":
    main()