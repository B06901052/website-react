import React from "react";
import styled from "styled-components";
import { useTable, useBlockLayout } from "react-table";
import { useSticky } from "react-table-sticky";

import makeData from "./makeData";

const Styles = styled.div`
  .table {
    outline: 1px solid #ddd;

    .th,
    .td {
      background-color: #fff;
      overflow: hidden;
    }

    &.sticky {
      overflow: scroll;
      .header,
      .footer {
        position: sticky;
        z-index: 1;
        width: fit-content;
      }

      .header {
        top: 0;
        box-shadow: 0px 3px 3px #ccc;
      }

      .footer {
        bottom: 0;
        box-shadow: 0px -3px 3px #ccc;
      }

      .body {
        position: relative;
        z-index: 0;
      }

      [data-sticky-td] {
        position: sticky;
      }

      [data-sticky-last-left-td] {
        box-shadow: 2px 2px 3px #ccc;
      }

      [data-sticky-first-right-td] {
        box-shadow: -2px -2px 3px #ccc;
      }
    }
  }
`;

function Table({ columns, data, height = "500px" }) {
  const defaultColumn = React.useMemo(
    () => ({
      minWidth: 10,
      width: 150,
      maxWidth: 400,
    }),
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable(
    {
      columns,
      data,
      defaultColumn,
    },
    useBlockLayout,
    useSticky
  );

  return (
    <Styles>
      <div
        {...getTableProps()}
        className="table sticky"
        style={{ width: "fit-content", maxWidth: "100%", maxHeight: height, margin: "auto" }}
      >
        <div className="header">
          {headerGroups.map((headerGroup) => (
            <div {...headerGroup.getHeaderGroupProps()} className="tr">
              {headerGroup.headers.map((column) => (
                <div {...column.getHeaderProps()} className="th">
                  {column.render("Header")}
                </div>
              ))}
            </div>
          ))}
        </div>

        <div {...getTableBodyProps()} className="body">
          {rows.map((row, i) => {
            prepareRow(row);
            return (
              <div {...row.getRowProps()} className="tr">
                {row.cells.map((cell) => {
                  return (
                    <div {...cell.getCellProps()} className="td">
                      {cell.render("Cell")}
                    </div>
                  );
                })}
              </div>
            );
          })}
        </div>
      </div>
    </Styles>
  );
}

function ExampleTable({data, ...props}) {
  let columns = Object.keys(data[0]).map((key) => {
    return {
      Header: key,
      accessor: key,
      width: key.toUpperCase() == key ? 60 : 100,
    };
  })
  columns[0]["sticky"] = "left";

  const memoColumns = React.useMemo(
    () => columns
  );
  
  const longerData = data.concat(data).concat(data);
  const memoData = React.useMemo(() => (longerData), []);

  return <Table columns={memoColumns} data={memoData} {...props} />;
}

export default ExampleTable;
