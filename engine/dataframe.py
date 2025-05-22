import polars as pl

def join(source_df: pl.DataFrame, target_df: pl.DataFrame, keys: list[str], how: str = "inner") -> pl.DataFrame:
  """
  Realiza o join entre dois DataFrames do Polars com base nas chaves fornecidas.

  Args:
    source_df (pl.DataFrame): DataFrame de origem.
    target_df (pl.DataFrame): DataFrame de destino.
    keys (list[str]): Lista de colunas usadas como chave para o join.
    how (str): Tipo de join a ser realizado. Pode ser "inner", "left", "outer", etc. (padrão: "inner").

  Returns:
      pl.DataFrame: DataFrame resultante do join.
  """
  try:
      # Padroniza os tipos de dados das chaves de join
    for key in keys:
      if key in source_df.columns:
        source_df = source_df.cast({key: pl.String})
      if key in target_df.columns:
        target_df = target_df.cast({key: pl.String})

    # Realiza o join com base nas chaves e no tipo especificado
    result_df = source_df.join(target_df, on=keys, how=how)
    return result_df
  except Exception as e:
    print(f"Erro ao realizar o join: {e}")
    return source_df  # Retorna um DataFrame vazio em caso de erro
  

__all__ = ["join"]